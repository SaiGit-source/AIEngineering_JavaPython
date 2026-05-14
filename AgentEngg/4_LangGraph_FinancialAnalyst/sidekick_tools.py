from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
import requests
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
import yfinance as yf


load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
    return "success"


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


def get_bank_metrics(ticker_symbol: str) -> str:
    """Fetches key financial ratios and stock metrics for a given bank ticker symbol."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Safely extract specific financial health metrics
        metrics = {
            "Bank Name": info.get("longName", ticker_symbol),
            "Current Price": info.get("currentPrice", "N/A"),
            "Trailing P/E Ratio": info.get("trailingPE", "N/A"),
            "Dividend Yield (%)": (info.get("dividendYield", 0) or 0) * 100,
            "Price to Book (P/B) Ratio": info.get("priceToBook", "N/A"),
            "Total Revenue": info.get("totalRevenue", "N/A"),
            "Return on Equity (ROE)": (info.get("returnOnEquity", 0) or 0) * 100
        }
        
        # Format the dictionary into a clean text block for the LLM to read
        result_text = f"--- Financial Data for {ticker_symbol} ---\n"
        for key, value in metrics.items():
            result_text += f"{key}: {value}\n"
        return result_text
        
    except Exception as e:
        return f"Error fetching metrics for {ticker_symbol}: {str(e)}"


async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, description="Use this tool when you want to send a push notification")
    file_tools = get_file_tools()

    tool_search =Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search"
    )

    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    python_repl = PythonREPLTool()
    
    finance_tool = Tool(
        name="fetch_bank_financial_metrics",
        func=get_bank_metrics,
        description="Input a bank stock ticker (e.g., 'RY.TO', 'TD.TO') to fetch key valuation ratios, dividend yields, and return on equity data."
    )
    
    return file_tools + [push_tool, tool_search, python_repl,  wiki_tool, finance_tool]

