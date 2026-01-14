from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate


load_dotenv()

## we need the web search tool

@tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4o")
tools = [get_current_date_time, search_tool]

prompt = PromptTemplate.from_template(
    """
    You are an AI assistant that can use tools.

    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    IMPORTANT:
        - Always follow the format exactly.
        - Always end with: Final Answer: ...

    Use the following format:

    Question: the input question {input} you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the tool
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """)


research_agent = create_react_agent(llm, [search_tool], prompt)

research_executor = AgentExecutor(agent=research_agent, tools=[search_tool], verbose=True)

@tool("research_web")
def research_web(query: str) -> str:
    """Use the research subagent to search the web and return a short answer."""
    result=research_executor.invoke({"input": query})
    return result["output"]

multi_tools = [get_current_date_time, research_web]

supervisor_agent = create_react_agent(llm, multi_tools, prompt)

supervisor_executor = AgentExecutor(agent=supervisor_agent, tools=multi_tools, verbose=True)

def chat(query: str) -> str:
    result = supervisor_executor.invoke({"input": query})
    return result["output"]


print(chat("Find which country hosted FIFA 2022 and also tell my current local time."))

## Supervisor agent uses the research subagent to get web results and also gets current date and time.

