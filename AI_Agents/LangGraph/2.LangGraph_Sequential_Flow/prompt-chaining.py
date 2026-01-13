
from langgraph.graph import StateGraph, START, END ## to create a graph we create with the help of StateGraph

from typing import TypedDict

### When using LLM, we need to import additional things
from langchain_openai import ChatOpenAI ## LLM model
from dotenv import load_dotenv ## to load environment variables from .env file

load_dotenv() ## loading the .env file

model = ChatOpenAI(model_name="gpt-4o") ## initializing the LLM model

## If you give me a topic, i will first create an outline and then write a Story based on that outline
## workflow is very similar to Dagster

class StoryState(TypedDict): ## we will store the state in the dictionary format
    topic: str
    outline: str
    story: str

def generate_outline_fun(state: StoryState) -> StoryState:
    prompt = f"Generate a detailed outline for a story on the topic {state['topic']}"
    outline = model.invoke(prompt).content ## using the LLM to generate an outline based on the topic
    state['outline'] = outline
    return state

def generate_story_fun(state: StoryState) -> StoryState:
    topic = state['topic']
    outline = state['outline']
    prompt = f"Write a 200 words detailed story based on the topic: {topic}, using the following outline:\n {outline}"
    story = model.invoke(prompt).content ## using the LLM to generate a story based on the outline
    state['story'] = story
    return state

graph = StateGraph(StoryState)
## i give a topic, LLM returns an outline

## Nodes
graph.add_node('generate_outline', generate_outline_fun)
graph.add_node('generate_story', generate_story_fun)

## Edges
graph.add_edge(START, 'generate_outline')
graph.add_edge('generate_outline', 'generate_story')
graph.add_edge('generate_story', END)

workflow = graph.compile() ## compiling the graph into a workflow

initial_state = {
    'topic': 'Write an essay on greatness of Java'
}

final_state = workflow.invoke(initial_state) ## invoking the workflow to run the graph

print(final_state) ## printing the final state after running the graph

png = workflow.get_graph().draw_mermaid_png()
with open("prompt-chaining.png", "wb") as f: 
    f.write(png)
