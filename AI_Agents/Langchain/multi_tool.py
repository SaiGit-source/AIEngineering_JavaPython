from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun

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

def chat(query: str) -> str:
    messages = []
    messages.append(HumanMessage(content=query))

    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
        
        if not ai_msg.tool_calls: ## when are we going to stop calling LLM, when ai_msg.tool_calls is empty, we can return content
            return ai_msg.content
                
        # Execute tool calls and add responses to messages
        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"]
            tool_input = tool_call["args"]
            tool_call_id = tool_call["id"]
            
            tool_function = next((t for t in tools if t.name == tool_name), None)
            tool_msg = tool_function.invoke(tool_input)
            messages.append(ToolMessage(content=tool_msg, tool_call_id=tool_call_id))
             
            ''' also works!!
            
            # Execute the appropriate tool
            if tool_name == "get_current_date_time":
                result = get_current_date_time.invoke(tool_input)
            elif tool_name == "duckduckgo_search":
                result = search_tool.invoke(tool_input["query"])
            else:
                result = "Unknown tool"
            
            # Add tool response to messages
            messages.append(ToolMessage(content=result, tool_call_id=tool_call_id))
            
            '''



response = chat("Current time in the country where Messi's debut match for the club took place on July 21, 2023, in a Leagues Cup game against Cruz Azul")
#response = chat("Current time in the country where Messi visited in Dec 2025")
#response = chat("Who is the founder of Coursera?")
print(response)

## Messi visited India in December 2025, starting his tour in Kolkata. The current date and time is 2025-12-22 16:43:52.
## Coursera was founded by Daphne Koller and Andrew Ng in 2012. They are both professors at Stanford University with expertise in computer science and artificial intelligence.
## In December 2025, Messi visited India. As for the current time in India, it is 2025-12-22 17:15:45.

'''
Lionel Messi made his club debut for Inter Miami in a Leagues Cup match against Cruz Azul on July 21, 2023. The match took place in Miami, USA.

The current date and time in Miami, USA is December 22, 2025, 17:24:02.
'''