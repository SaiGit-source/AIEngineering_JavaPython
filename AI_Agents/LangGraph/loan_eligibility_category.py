## Simple LangGraph without LLM for learning purposes

from langgraph.graph import StateGraph, START, END ## to create a graph we create with the help of StateGraph

from typing import TypedDict

#graph = StateGraph()

#graph.add_node("Node1")
#graph.add_node("Node2")
#graph.add_edge("Node1", "Node2") ## first edge is between Start and Node1


## Start --> Node1 --> Node2 --> End
## We need 4 nodes. Start and End nodes are given by LangGraph by default


## Whenever we are jumping from one node to another, they will be sharing this particular state like in React useState()
class LoanState(TypedDict):
    age: int
    income: float
    eligible: bool
    max_loan: float
    category: str ## one more node
    
    
## What's the sole purpose of this function?
def calc_eligibility(state: LoanState) -> LoanState:
    ## Between the Start and End nodes, what should change? State
    ## job of this function is to change state
    ## This function accepts a state and returns a state
    income = state['income']
    age = state['age']
    eligible = income >= 30000 and 21 <= age <= 65
    max_loan = income * 5 if eligible else 0.0
    state['eligible'] = eligible
    state['max_loan'] = max_loan ## Here we are changing the max_loan in the state
    return state


def label_category(state: LoanState) -> LoanState:
    income = state['income']
    eligible = state['eligible']
    if not eligible:
        category = 'Not Eligible'
    elif income < 50000:
        category = 'Basic loan'
    elif income < 100000:
        category = 'Premium loan'
    else:
        category = 'Elite loan'   
    state['category'] = category ## here we are changing the category in the state
    return state


graph = StateGraph(LoanState) ## specifying the type of state the graph will be using

graph.add_node("calc_eligibility", calc_eligibility) ## adding a node to calculate eligibility
graph.add_node("label_category", label_category) ## adding a node to label category based on eligibility and income
graph.add_edge(START, 'calc_eligibility') ## first edge is between Start and calc_eligibility
graph.add_edge('calc_eligibility', 'label_category') ## second edge is between calc_eligibility and label_category
graph.add_edge('label_category', END) ## last edge is between label_category and End

workflow = graph.compile() ## compiling the graph into a workflow
initial_state: LoanState = {
    'age': 30,
    'income': 5000,
    'eligible': False,
    'max_loan': 0.0
} ## initial state to start the workflow

final_state = workflow.invoke(initial_state) ## invoking the workflow to run the graph

print(final_state) ## printing the final state after running the graph

## Output {'age': 30, 'income': 50000, 'eligible': True, 'max_loan': 250000, 'category': 'Premium loan'}

## Why we need to do this entire flow if we can run a normal Python function
## It is a learning exercise to understand how LangGraph works under the hood

png = workflow.get_graph().draw_mermaid_png() ## getting the graphviz representation of the graph
with open("AI_Agents\LangGraph\loan_eligibility_cat_graph.png", "wb") as f:
    f.write(png)
    
## In this workflow, we dont have AI, we need AI though

