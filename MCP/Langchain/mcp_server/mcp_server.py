from fastmcp import FastMCP
from datetime import datetime
from langchain_community.tools import DuckDuckGoSearchRun


mcpServer = FastMCP("TestMCPServer")

## mcpServer needs to have some primitives, Tools, resources, prompts


@mcpServer.tool("get_current_date_time")
def get_current_date_time() -> str:
    """Get the current date and time in the format YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = DuckDuckGoSearchRun()

@mcpServer.tool("web_search")
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo search."""
    search_results = search_tool.invoke({"query": query})
    return search_results

## Lets use remote one here

mcpServer.run(transport="sse", host="localhost", port=8000)



