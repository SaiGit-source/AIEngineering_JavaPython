from dataclasses import dataclass
from autogen_core import AgentId
import glob
import os
import requests
import yfinance as yf
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
import random

load_dotenv(override=True)

@dataclass
class Message:
    content: str


def find_recipient() -> AgentId:
    # clones are going to be named: Agent1, Agent2, etc. This function finds all agents in the system and randomly selects one to bounce the idea off of. You can implement your own logic to find a recipient based on specialties, past interactions, or any other criteria you choose.
    try:
        agent_files = glob.glob("agent*.py")
        print(f"Scanning folder: {os.getcwd()}")
        agent_names = [os.path.splitext(file)[0] for file in agent_files]
        # basically looks into the directory to see what agents are available to bounce the idea off of. It assumes that all agents are in the same directory and are named in a way that starts with "agent". You can modify this logic to fit your specific project structure and naming conventions.
        agent_names.remove("AgentTemplate")
        agent_name = random.choice(agent_names)
        print(f"Selecting agent for refinement: {agent_name}")
        return AgentId(agent_name, "default")
    except Exception as e:
        print(f"Exception finding recipient: {e}")
        return AgentId("agent1", "default")
    


async def get_stock_info(ticker: str) -> dict:
    """
    Get financial information for a stock ticker.
    """

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "ticker": ticker,
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "current_price": info.get("currentPrice"),
        "pe_ratio": info.get("trailingPE"),
        "beta": info.get("beta"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow")
    }



FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    
async def get_stock_quote(ticker: str) -> dict:
    """
    Get real-time stock quote from Finnhub.
    """
    url = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": ticker,
        "token": FINNHUB_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    return {
        "ticker": ticker,
        "current_price": data.get("c"),
        "high_price": data.get("h"),
        "low_price": data.get("l"),
        "open_price": data.get("o"),
        "previous_close": data.get("pc")
    }
    
serper = GoogleSerperAPIWrapper()

async def web_search(query: str) -> str:
        """
        Use this tool to perform an online web search for
        financial news, stock analysis, earnings, or market trends.
        """

        results = serper.run(query)

        return results
    