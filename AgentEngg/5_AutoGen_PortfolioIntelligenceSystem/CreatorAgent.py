from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
from autogen_core import TRACE_LOGGER_NAME
import importlib
import logging
from autogen_core import AgentId
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# this is the Agent that creates and spawns Agents. 
class Creator(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """

        You are a Creator Agent that generates specialized AI agents for a multi-agent financial portfolio analysis system.

        You receive a Python agent template using AutoGen Core and AutoGen AgentChat. Your job is to generate new Agent classes from that template while preserving the required class structure, imports, inheritance, method signatures, and runtime compatibility.

        Every generated agent must be focused only on stock market portfolio analysis, especially technology-focused portfolios.

        You may generate N different agents. Each generated agent should have a unique specialization, personality, and analytical perspective.

        Possible portfolio agent specializations include:
        - MarketResearchAgent: analyzes latest financial news, earnings, product launches, and market catalysts.
        - StockFundamentalsAgent: analyzes revenue growth, margins, PE ratio, valuation, balance sheet strength, and profitability.
        - TechnicalAnalysisAgent: analyzes price trends, momentum, moving averages, RSI, MACD, support/resistance, and chart patterns.
        - PortfolioRiskAgent: analyzes concentration risk, volatility, correlation, beta, drawdown, and downside exposure.
        - SentimentAnalysisAgent: analyzes news sentiment, investor sentiment, analyst tone, and market narratives.
        - MacroEconomicAgent: analyzes interest rates, inflation, central bank policy, bond yields, and macro risks affecting tech stocks.
        - SectorAllocationAgent: analyzes diversification across AI, cloud, cybersecurity, semiconductors, software, and consumer tech.
        - ComplianceAgent: reviews outputs for unsafe claims, overconfidence, missing risk disclosures, and financial advice concerns.
        - ReportWriterAgent: synthesizes all agent outputs into a clear final portfolio report.

        Generated agents should use available tools when relevant, such as:
        - Serper or web search for recent market news
        - Stock quote tools for price data
        - Fundamental data tools for valuation and financial metrics
        - Historical price tools for volatility and return analysis
        - Sentiment tools for news sentiment
        - Custom portfolio analysis tools for allocation and risk calculations

        Generated agents must not hardcode portfolio holdings, stock choices, or allocations. They should use available tools and reasoning to analyze or propose portfolios.

        Each generated agent should:
        - Stay strictly within finance, investing, stock market analysis, technology portfolios, and portfolio risk management.
        - Avoid non-financial topics.
        - Avoid guaranteed buy/sell recommendations.
        - Clearly mention uncertainty and risk.
        - Provide structured reasoning.
        - Collaborate with other agents by reviewing, challenging, refining, or complementing their analysis.
        - Produce practical insights that can contribute to a final portfolio report.

        When generating code:
        - The class must be named Agent.
        - The class must inherit from RoutedAgent.
        - The __init__ method must take a name parameter.
        - Do not change required method signatures.
        - Keep compatibility with AutoGen Core message routing.
        - Preserve the template structure unless a change is necessary for specialization.
        - Respond only with valid Python code.
        - Do not include markdown, explanations, or extra text.
            """


    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=1.0)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message, tools=[messages.get_stock_info, messages.get_stock_quote, messages.web_search]) # you can add more tools here that the Creator agent can use when generating new agents. These tools will be available for the Creator agent to use in its reasoning process when it is generating new agents. The tools are defined in the messages.py file and can include functions for getting stock information, getting stock quotes, performing web searches, or any other relevant financial analysis tools that you want the Creator agent to have access to when it is generating new agents.   

    def get_user_prompt(self):
        prompt = "Please generate a new Agent based strictly on this template. Stick to the class structure. \
            Respond only with the python code, no other text, and no markdown code blocks.\n\n\
            Be creative about taking the agent in a new direction, but don't change method signatures.\n\n\
            Here is the template:\n\n"
        with open("AgentTemplate.py", "r", encoding="utf-8") as f:
            template = f.read()
        return prompt + template   
        

    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        filename = message.content
        agent_name = filename.split(".")[0]
        text_message = TextMessage(content=self.get_user_prompt(), source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.chat_message.content) # it saves as Agent1, Agent2, Agent3, etc. based on the filename that is sent in the message content. The filename is expected to be in the format "AgentX.py" where X is a unique identifier for the agent. You can modify this logic to fit your specific naming conventions or project structure.
        print(f"** Creator has created python code for agent {agent_name} - about to register with Runtime")
        module = importlib.import_module(agent_name) # import the Python module (agent5.py) it just wrote. it gets the agent_name from messages. agent_name = filename.split(".")[0]
        await module.Agent.register(self.runtime, agent_name, lambda: module.Agent(agent_name)) # lambda function will spawn a new instance, a factory method that will create a new instance of that agent on demand. 
        logger.info(f"** Agent {agent_name} is live")
        result = await self.send_message(messages.Message(content="Give me a nice portfolio with analysis, tools used and explanation"), AgentId(agent_name, "default")) 
        # it will send message to that agent, give me an idea, to test if the agent is working. It sends a message to the newly created agent to test if it's working. The message content is "Give me an idea", but you can modify this to fit your specific testing needs.
        # that will trigger that agent, will get that message and process that idea, work on that idea and potentially if probability meets the criteria, it will send on its idea to another agent that it will find in the directory, and ask the other agent to add feedback to it. It demonstrates AutoGenCore's power as an Agent messaging platform, it allows for this kind of inter-process communication without having to worry about details.
        return messages.Message(content=result.content)