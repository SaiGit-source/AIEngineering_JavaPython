from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent

load_dotenv()

## we need the web search tool

@tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4o")
tools = [get_current_date_time, search_tool]
llm_with_tools = llm.bind_tools(tools=tools)

prompt = PromptTemplate.from_template(
    """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """)
## https://smith.langchain.com/hub/hwchase17/react
### or prompt = client.pull_prompt("hwchase17/react")


agent = create_agent(model=llm, tools=tools, system_prompt="You are a helpful AI agent that uses tools to answer user queries.")


def chat(query: str) -> str:
    ## we replace all content with an agent
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result


#response = chat("Current time in the country where Messi's debut match for the club took place on July 21, 2023, in a Leagues Cup game against Cruz Azul")
response = chat("Current time in the country where Messi visited in Dec 2025")
#response = chat("Who is the founder of Coursera?")
#print(response["messages"][-1].content)
print(response)
