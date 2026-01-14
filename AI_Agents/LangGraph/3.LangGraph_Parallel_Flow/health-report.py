
from langgraph.graph import StateGraph, START, END ## to create a graph we create with the help of StateGraph

from typing import TypedDict, Annotated ## to create typed dictionaries for state management

### When using LLM, we need to import additional things
from langchain_openai import ChatOpenAI ## LLM model
from dotenv import load_dotenv ## to load environment variables from .env file
from pydantic import BaseModel, Field ## to create structured output
import operator     ## to perform operations like addition, subtraction, etc.

load_dotenv() ## loading the .env file

model = ChatOpenAI(model_name="gpt-4o")

### When you do a prompt, it will give you simple sentence. But if you want a structured output, you need to work with it.
### How to get structured output from AI? to do that, we use PyDantic
### We are doing this to get output in a particular JSON format, not in a lengthy string. So we create a schema for that.
class HealthSchema(BaseModel):
    metric_name: str = Field(description="Name of the health metric (e.g., BMI, BMR, Calories)")
    value: float = Field(description="Numerical value of the health metric")
    explanation: str = Field(description="Brief explanation of the health metric")  

structured_model = model.with_structured_output(HealthSchema) ## structured model for structured output    
## whenever you want a structured output, you can use structured_model instead of model. for normal conversation use model.

class HealthState(TypedDict):
    age: int
    weight: float
    height: float
    activity_level: str
    bmi_feedback: str
    bmr_feedback: str
    calories_feedback: str
    overall_report: str
    individual_values: Annotated[list[float], operator.add] ## add values that are getting appended to this list, not replace. by default, it will get replaced
    
    
## why we are doing calculations in parallel? Because all these calculations can be done individually on the state.
    
## Create nodes
## Here calculate_bmi, calculate_bmr, and calculate_calories are independent of each other and will run in parallel. 
# but they share the same state (HealthState). So LangGraph says sharing state will create issues and conflicts.
## Therefore instead of modifying the same state, we will return only values like bmi value, bmr value, calories value from each function.

def calculate_bmi(state: HealthState) -> HealthState:
    prompt = f"Calculate the BMI for a person with weight {state['weight']} kg and height {state['height']} cm. Provide the value and a brief explanation."
    feedback = structured_model.invoke(prompt)
    #state['bmi_feedback'] = feedback
    #state['individual_values'].append(feedback.values)
    #return state
    return {'bmi_feedback': feedback.explanation, 'individual_values': [feedback.value]} ## return only modified parts

def calculate_bmr(state: HealthState) -> HealthState:
    prompt = f"Calculate the BMR for a person aged {state['age']} years, weighing {state['weight']} kg and height {state['height']} cm. Provide the value and a brief explanation."
    feedback = structured_model.invoke(prompt)
    return {'bmr_feedback': feedback.explanation, 'individual_values': [feedback.value]} ## return only modified parts

def calculate_calories(state: HealthState) -> HealthState:
    prompt = f"Calculate the daily calorie needs for a person aged {state['age']} years, weighing {state['weight']} kg, height {state['height']} cm, and with an activity level of {state['activity_level']}. Provide the value and a brief explanation."
    feedback = structured_model.invoke(prompt)
    return {'calories_feedback': feedback.explanation, 'individual_values': [feedback.value]} ## return only modified parts


def generate_overall_report(state: HealthState) -> HealthState:
    prompt = f"Based on the following feedbacks:\nBMI: {state['bmi_feedback']}\nBMR: {state['bmr_feedback']}\nCalories: {state['calories_feedback']}\nGenerate an overall comprehensive health report."
    report = model.invoke(prompt).content ## here we dont need structured_model, normal model is fine
    #state['overall_report'] = feedback
    #return state
    return {'overall_report': report} ## return only modified parts

graph = StateGraph(HealthState) ## create a state graph with HealthState
graph.add_node('calculate_bmi', calculate_bmi) ## second 'calculate_bmi' refers to the name of the function created above
graph.add_node('calculate_bmr', calculate_bmr)
graph.add_node('calculate_calories', calculate_calories)
graph.add_node('generate_overall_report', generate_overall_report)      


# edges 
## Parallel workflow
graph.add_edge(START, 'calculate_bmi')
graph.add_edge(START, 'calculate_bmr')
graph.add_edge(START, 'calculate_calories')
graph.add_edge('calculate_bmi', 'generate_overall_report')
graph.add_edge('calculate_bmr', 'generate_overall_report')
graph.add_edge('calculate_calories', 'generate_overall_report')
graph.add_edge('generate_overall_report', END)

workflow = graph.compile() ## compiling the graph into a workflow

initial_state = {
    'age': 35,
    'weight': 83.0,
    'height': 183.0,
    'activity_level': 'moderate',
    'bmi_feedback': '',
    'bmr_feedback': '',
    'calories_feedback': '',
    'overall_report': '',
    'individual_values': []
}

final_state = workflow.invoke(initial_state) ## invoking the workflow to run the graph

print(final_state) ## printing the final state after running the graph

png = workflow.get_graph().draw_mermaid_png()
with open("health-report.png", "wb") as f:
    f.write(png)


### Output:
## {'age': 35, 'weight': 83.0, 'height': 183.0, 'activity_level': 'moderate', 'bmi_feedback': "BMI (Body Mass Index) is a measure used to determine if a person has a healthy body weight for a given height. It is calculated by dividing a person's weight in kilograms by the square of their height in meters. A BMI between 18.5 and 24.9 is considered normal, suggesting a healthy weight. Beyond this range, individuals may be classified as underweight, overweight, or obese, indicating potential health risks.", 'bmr_feedback': 'The Basal Metabolic Rate (BMR) is an estimate of how many calories your body would burn if you were at rest all day. It is a crucial metric for understanding the minimum calorie intake needed to maintain basic physiological functions such as breathing, circulation, and cell production. BMR varies based on several factors, including age, weight, height, and sex.', 'calories_feedback': "This estimate is based on the Mifflin-St Jeor Equation and considers the person's Basal Metabolic Rate (BMR) combined with their activity level.      