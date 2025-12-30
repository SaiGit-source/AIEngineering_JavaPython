## i want to talk to LLM, and if LLM says i want to create a file in a folder and write some contents
### we can take help from MCP server FileSystem
## instead of single thread, we can use Async calls to make it faster

import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient ## in this you provide, which server to connect and this library will take care of connecting to multiple MCP servers
## to work with NodeJS you need Platform module
import platform

prompt = "Create a file named 'testMCP.txt' in the folder 'MCP_Test_Folder' and write 'Hello from MCP! MCP Test successful' into it. Then read the contents of the file and return it."
MCP_FOLDER = r"C:/Users/saito/source/repos/AIEngineering_JavaPython/MCP/Langchain/MCP_Test_Folder"
load_dotenv()

def npx_command():
    return "npx" if platform.system() != "Windows" else "npx.cmd"

async def chat(query: str) -> str:
   client = MultiServerMCPClient({
    "filesystem": {
        "transport": "stdio", ## for local MCP server, we use stdio
        "command": npx_command(),
        "args": ["-y", "@modelcontextprotocol/server-filesystem", MCP_FOLDER]   
   }
   })
   
   tools = await client.get_tools() ## await the async function
   llm = ChatOpenAI(model="gpt-4o", temperature=0)
   llm_with_tools = llm.bind_tools(tools=tools)


   messages = []
   messages.append(SystemMessage(content=f"You are an expert file system assistant. All file operations must be performed in {MCP_FOLDER}"))
   messages.append(HumanMessage(content=query))

## LLM chat will go in a loop
   while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
        ## How will you know LLM is trying for a tool call? if it is a tool call, it will have data in the tool calls array
        ## if tool calls array is empty, thats when we know it is the final response/message
        if ai_msg.tool_calls == []:
            return ai_msg.content
        
        ### if tool_calls array is not empty, we have to see which tool we have to call
        
        for tc in ai_msg.tool_calls:
            tool_name = tc["name"]
            tool_input = tc["args"]
            tool_call_id = tc["id"]
            
            tool_function = next((t for t in tools if t.name == tool_name), None)
            tool_msg = await tool_function.ainvoke(tool_input) ## async invoke
            messages.append(ToolMessage(content=tool_msg, tool_call_id=tool_call_id))

response = asyncio.run(chat(prompt))        


   
   
   