import asyncio
from contextlib import AsyncExitStack

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import os

load_dotenv(override=True)

MAX_TURNS = 20
print("TAVILY KEY LOADED:", bool(os.getenv("TAVILY_API_KEY")))
print("TAVILY KEY PREFIX:", os.getenv("TAVILY_API_KEY", "")[:6])

CARD_MCP_SERVER_PARAMS = {
    "command": "uv",
    "args": ["run", "card_mcp_server.py"],
}


WEB_SEARCH_MCP_SERVER_PARAMS = {
    "command": "npx",
    "args": [
        "-y",
        "mcp-remote",
        f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY', '')}",
    ],
}

def credit_analyst_instructions() -> str:
    return """
You are a Credit Analyst Agent for a simulated banking credit-card system.

Your job:
1. Review the customer's credit profile.
2. Review recent card transactions.
3. Review payment history.
4. Research current economic or consumer-credit context using available web search tools.
5. Decide whether to Increase, Decrease, keep No Change, or send to Manual Review.
6. Save the decision using the save_credit_decision tool.
7. Write an audit log using write_audit_log.

Decision guidelines:
- Increase if credit score >= 700, utilization < 40%, late payments = 0, risk indicators are low, and external economic context is not concerning.
- Manual Review if risk is moderate, utilization is between 50% and 90%, there is 1 late payment, or external credit-risk conditions appear uncertain.
- Decrease if utilization > 90%, late payments >= 2, credit score < 620, or risky indicators are high.
- No Change if customer is acceptable but does not strongly qualify for increase.

External research guidance:
- Search for current consumer credit risk, credit-card delinquency trends, interest-rate context, household debt risk, or bank credit tightening.
- Use external research as supporting context only.
- Do not let external research override severe customer-level risk.
- Mention the economic context briefly in the reasoning summary.

Risk score:
- Return a score from 0 to 100.
- Low risk: 0-30.
- Medium risk: 31-70.
- High risk: 71-100.

Important:
- Always call get_credit_profile.
- Always call get_recent_transactions.
- Always call get_payment_history.
- Always use web search at least once.
- Always call save_credit_decision.
- Always call write_audit_log.
- Do not claim this is a real bank decision.
- This is a simulation.
"""

async def run_credit_analyst_agent_async() -> str:
    async with AsyncExitStack() as stack:
        card_mcp_server = await stack.enter_async_context(
            MCPServerStdio(
                CARD_MCP_SERVER_PARAMS,
                client_session_timeout_seconds=120,
            )
        )

        web_search_mcp_server = await stack.enter_async_context(
            MCPServerStdio(
                WEB_SEARCH_MCP_SERVER_PARAMS,
                client_session_timeout_seconds=120,
            )
        )

        agent = Agent(
            name="Credit Analyst Agent",
            instructions=credit_analyst_instructions(),
            model="gpt-4o-mini",
            mcp_servers=[
                card_mcp_server,
                web_search_mcp_server,
            ],
        )

        result = await Runner.run(
            agent,
            """
Review the current customer's credit-card profile and make a credit-limit decision.

You must:
1. Use the banking MCP tools to gather the profile, transactions, and payment history.
2. Use the web search MCP tools to research current consumer credit risk, credit-card delinquency, interest-rate, or household debt context.
3. Decide Increase, Decrease, No Change, or Manual Review.
4. Save the decision using save_credit_decision.
5. Write an audit log.
6. Return a concise summary with decision, old limit, new limit, risk score, economic context, and reasoning.
""",
            max_turns=MAX_TURNS,
        )

        return result.final_output

def run_credit_analyst_agent() -> str:
    return asyncio.run(run_credit_analyst_agent_async())


if __name__ == "__main__":
    print(run_credit_analyst_agent())