from typing_extensions import runtime

from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
from AgentTemplate import Agent
from CreatorAgent import Creator
from EvaluatorAgent import ReportEvaluatorAgent
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from autogen_core import AgentId
import messages
import asyncio

# HOW_MANY_AGENTS = 20
HOW_MANY_AGENTS = 2

async def create_and_message(worker, creator_id, i: int, all_agent_outputs: list): # takes-in a worker, creator_id and an integer i (Agent number 1,2,3,4,5). 
    # The worker is the runtime that will be used to send messages and register agents. 
    # The creator_id is the AgentId of the Creator agent, which is responsible for creating new agents. The integer i is used to generate unique filenames for the new agents and their corresponding idea files.
    # it's going to hit real APIs, it is going to cost like 2 cents
    # The Agent creator could decide to use an expensive model instead of gpt-4o-mini, and then the cost would go up. Be mindful of that when you run this code, especially if you increase the number of agents.
    
    try:
        result = await worker.send_message(messages.Message(content=f"agent{i}.py"), creator_id)
        
        # FIX: Added encoding="utf-8" to prevent the 'charmap' codec encoding crash
        with open(f"portfolio{i}.md", "w", encoding="utf-8") as f:
            all_agent_outputs.append(
                f"\n=========================\nAgent {i} Portfolio Analysis\n=========================\n{result.content}\n"
            )
            f.write(result.content)
            
    except Exception as e:
        print(f"Failed to run worker {i} due to exception: {e}")
        
async def create_evaluation_report(
        worker,
        report_evaluator_id,
        all_agent_outputs
    ):
    try:
        combined_analysis = "\n\n".join(all_agent_outputs)

        prompt = f"""
        Here are the portfolio analyses created by the specialist agents.

        Please evaluate them and create the consolidated final technology portfolio report.

        Agent Outputs:

        {combined_analysis}
        """

        result = await worker.send_message(
                messages.Message(content=prompt),
                report_evaluator_id
            )

        with open("final_report.md", "w", encoding="utf-8") as f:
            f.write(result.content)

        print("Final portfolio report created successfully.")

        return result.content

    except Exception as e:
        print(f"Failed to create evaluation report due to exception: {e}")
        return None        

async def main():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051") # creates a GrpcWorkerAgentRuntimeHost host
    host.start() # starts host
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    result = await Creator.register(worker, "Creator", lambda: Creator("Creator")) # register creator agent with runtime. It registers the Creator agent with the runtime, which allows it to receive messages and create new agents. The Creator agent is responsible for generating new agents based on a template and sending them messages to test if they are working.
    creator_id = AgentId("Creator", "default") 
    
    await ReportEvaluatorAgent.register(worker,"ReportEvaluatorAgent", lambda: ReportEvaluatorAgent("ReportEvaluatorAgent"))
    report_evaluator_id = AgentId("ReportEvaluatorAgent", "default")
    all_agent_outputs = [] 
    coroutines = [create_and_message(worker, creator_id, i, all_agent_outputs) for i in range(1, HOW_MANY_AGENTS+1)]
    # we dont put await for coroutines as usual because we dont want to run them wait in a sequential manner, we want to run them concurrently. So we gather all the coroutines in a list and then we use asyncio.gather to run them concurrently. This allows us to create and message multiple agents at the same time, which can speed up the process significantly, especially if we are creating a large number of agents.
    # we are gathering a whole list of coroutines then i await them using asyncio.gather. asyncio.gather will run all the coroutines concurrently and wait for all of them to finish. This is more efficient than running them sequentially, especially if the operations involve waiting for I/O or network responses, which is likely the case here since we are sending messages to agents that may be processing ideas and potentially bouncing them off other agents.
    # they are not running like multi-threading, instead they are running in an event-loop so everytime they are waiting on Open-AI, which means it's waiting on a network connection, another one can be running and that means, they all get to run at the same time. 
    await asyncio.gather(*coroutines)
    await create_evaluation_report(worker, report_evaluator_id, all_agent_outputs)
    try:
        await worker.stop()
        await host.stop()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())


