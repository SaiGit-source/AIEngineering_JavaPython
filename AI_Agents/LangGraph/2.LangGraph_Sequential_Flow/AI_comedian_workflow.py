
from langgraph.graph import StateGraph, START, END ## to create a graph we create with the help of StateGraph

from typing import TypedDict

### When using LLM, we need to import additional things
from langchain_openai import ChatOpenAI ## LLM model
from dotenv import load_dotenv ## to load environment variables from .env file

load_dotenv() ## loading the .env file

model = ChatOpenAI(model_name="gpt-4o") ## initializing the LLM model

## If you give me a topic, i will give you a joke on that topic. So two things: Topic and Joke

class JokeState(TypedDict):
    topic: str
    joke: str
    
def comedian_fun(state: JokeState) -> JokeState:
    prompt = f"Tell me a joke about {state['topic']}"
    joke = model.invoke(prompt) ## using the LLM to generate a joke based on the topic
    state['joke'] = joke
    return state

graph = StateGraph(JokeState)
## i give a topic, LLM returns a Joke

graph.add_node('comedian', comedian_fun)
graph.add_edge(START, 'comedian')
graph.add_edge('comedian', END)


workflow = graph.compile() ## compiling the graph into a workflow

initial_state = {
    'topic': 'startups'
}

final_state = workflow.invoke(initial_state) ## invoking the workflow to run the graph

print(final_state) ## printing the final state after running the graph

png = workflow.get_graph().draw_mermaid_png()
with open("AI_Agents\LangGraph\AI_comedian_workflow.png", "wb") as f:
    f.write(png)
    
    
### Output
# content='Why did the startup founder bring a ladder to the meeting?\n\nBecause they heard the company had potential for high returns!'

'''
{'topic': 'startups', 'joke': AIMessage(content='Why did the startup founder bring a ladder to the meeting?\n\nBecause they heard the company had potential for high returns!', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 23, 'prompt_tokens': 13, 'total_tokens': 36, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_deacdd5f6f', 'id': 'chatcmpl-CxS9gUQZXfcGvE8DdzJ0XSOdCa6aS', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019bb609-175f-7fe1-bb52-5ac51457cb1b-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 13, 'output_tokens': 23, 'total_tokens': 36, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})}
'''
