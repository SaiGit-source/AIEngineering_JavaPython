
from langgraph.graph import StateGraph, START, END ## to create a graph we create with the help of StateGraph

from typing import TypedDict, Literal

### When using LLM, we need to import additional things
from langchain_openai import ChatOpenAI ## LLM model
from dotenv import load_dotenv ## to load environment variables from .env file
from pydantic import BaseModel, Field ## to create structured output
import operator     ## to perform operations like addition, subtraction, etc.

load_dotenv() ## loading the .env file

model = ChatOpenAI(model_name="gpt-4o")

## for each of these categories ('Underweight'), we need an advice function
class BMICategorySchema(BaseModel):
    category: Literal['Underweight', 'Normalweight', 'Overweight', 'Obesity'] = Field(description="BMI Category")
    explanation: str = Field(description="Brief explanation of the BMI category")
    
class HealthAdviceSchema(BaseModel):
    status: str = Field(description="Health status based on BMI")
    recommendation: str = Field(description="Health recommendation based on BMI")
    
class BMIValueSchema(BaseModel):
    value: float = Field(description="Numerical value of the BMI")
    
### Create structured models for structured output
bmi_value_model = model.with_structured_output(BMIValueSchema) ## structured model for BMI value
bmi_category_model = model.with_structured_output(BMICategorySchema) ## structured model for BMI category
health_advice_model = model.with_structured_output(HealthAdviceSchema) ## structured model for health advice

## State definition
class BMIState(TypedDict):
    weight: float ## Input
    height: float  ## Input
    bmi_value: float
    bmi_category: Literal['Underweight', 'Normalweight', 'Overweight', 'Obesity'] ## conditional edge
    bmi_explanation: str ## conditional edge
    response: str
    
## Only BMI here no BMR or Calorie
## Node functions
def calculate_bmi(state: BMIState) -> BMIState:
    prompt = f"Calculate the BMI for a person with weight {state['weight']} kg and height {state['height']} cm. Provide the value only"
    feedback = bmi_value_model.invoke(prompt)
    bmi_value = float(feedback.value) 
    return {'bmi_value': bmi_value} ## return only modified parts

def find_category(state: BMIState) -> BMIState:
    prompt = f"The BMI value is {state['bmi_value']}. Determine the BMI category (Underweight, Normalweight, Overweight, Obesity). Provide only the category."
    response = bmi_category_model.invoke(prompt)
    return {'bmi_category': response.category, 'bmi_explanation': response.explanation} ## return only modified parts

# router function to check category and route accordingly
def check_category(state: BMIState) -> Literal['Underweight', 'Normalweight', 'Overweight', 'Obesity']:
    return state['bmi_category']

## for each of these categories ('Underweight'), we need an advice function
def underweight_advice(state: BMIState) -> BMIState:
    prompt = f"The BMI value is {state['bmi_value']}. Provide health advice for someone who is underweight."
    advice = health_advice_model.invoke(prompt)
    response = f"""BMI: {state['bmi_value']} - {state['bmi_category'].upper()}
    Status: {advice.status}
    Recommendation: {advice.recommendation}
    """
    return {'response': response} ## return only modified parts

def normal_weight_advice(state: BMIState) -> BMIState:
    prompt = f"The BMI value is {state['bmi_value']}. Provide health advice for someone who has normal weight and for maintenance."
    advice = health_advice_model.invoke(prompt)
    response = f"""BMI: {state['bmi_value']} - {state['bmi_category'].upper()}
    Status: {advice.status}
    Recommendation: {advice.recommendation}
    """
    return {'response': response} ## return only modified parts

def overweight_advice(state: BMIState) -> BMIState:
    prompt = f"The BMI value is {state['bmi_value']}. Provide health advice for someone who is overweight."
    advice = health_advice_model.invoke(prompt)
    response = f"""BMI: {state['bmi_value']} - {state['bmi_category'].upper()}
    Status: {advice.status}
    Recommendation: {advice.recommendation}
    """
    return {'response': response} ## return only modified parts

def obesity_advice(state: BMIState) -> BMIState:
    prompt = f"The BMI value is {state['bmi_value']} (obese). Provide health advice for someone who has obesity including medical consultation."
    advice = health_advice_model.invoke(prompt)
    response = f"""BMI: {state['bmi_value']} - {state['bmi_category'].upper()}
    Status: {advice.status}
    Recommendation: {advice.recommendation}
    """
    return {'response': response} ## return only modified parts

graph = StateGraph(BMIState) ## create a state graph with BMIState
graph.add_node('calculate_bmi', calculate_bmi) ## second 'calculate_bmi' refers to the name of the function created above
graph.add_node('find_category', find_category)
graph.add_node('underweight_advice', underweight_advice)
graph.add_node('normal_weight_advice', normal_weight_advice)
graph.add_node('overweight_advice', overweight_advice)
graph.add_node('obesity_advice', obesity_advice)

# edges
## Conditional workflow
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', 'find_category')

## Conditional edges - Mapping categories to respective advice nodes
### after find category, is the router 'check_category'
graph.add_conditional_edges('find_category', check_category, {
    'Underweight': 'underweight_advice',
    'Normalweight': 'normal_weight_advice',
    'Overweight': 'overweight_advice',
    'Obesity': 'obesity_advice'
})

graph.add_edge('underweight_advice', END)
graph.add_edge('normal_weight_advice', END)
graph.add_edge('overweight_advice', END)
graph.add_edge('obesity_advice', END)
workflow = graph.compile() ## compiling the graph into a workflow
initial_state = {
    'weight': 70.0,
    'height': 170.0,
    'bmi_value': 0.0,
    'bmi_category': '',
    'bmi_explanation': '',
    'response': ''
}
final_state = workflow.invoke(initial_state) ## invoking the workflow to run the graph
print(final_state) ## printing the final state after running the graph

png = workflow.get_graph().draw_mermaid_png()
with open("bmi-conditional.png", "wb") as f:
    f.write(png)
