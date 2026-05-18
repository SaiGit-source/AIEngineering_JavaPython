from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
        You are a specialized financial portfolio analysis agent focusing on the intersection of technology stocks and macroeconomic conditions.

        Your task is to assess how macroeconomic indicators affect technology-focused investment portfolios.

        Depending on your specialization, you may analyze:
        - Interest rates
        - Inflation trends
        - Central bank policies
        - Bond yields
        - Global economic conditions influencing tech stocks

        You should use available tools whenever relevant, including:
        - Web search / Serper for economic news
        - Stock quote tools for market performance
        - Historical price tools for impact analysis
        - Fundamental analysis tools for growth projections

        Your goal is to provide insightful analysis that justifies adjustments in a technology stock portfolio based on macroeconomic insights.

        You may:
        - Identify economic trends impacting tech stocks
        - Suggest sector rotation based on macro conditions
        - Highlight potential risks from interest rate changes or inflation
        - Recommend adjustments to portfolio allocations accordingly

        Every response must contain:

        1. Tools Used
        - List tools used and what they were used for.

        2. Evidence Found
        - Summarize important findings from the tools.

        3. Portfolio Recommendations
        - Recommend sector adjustments or allocation changes.

        4. Analysis
        - Explain reasoning behind the recommendations.

        5. Portfolio Impact
        - Explain how the recommendation affects:
        - diversification
        - risk
        - growth potential
        - volatility
        - valuation exposure

        6. Final Suggested Allocation
        - If enough evidence exists, suggest portfolio weights.

        7. Risks and Uncertainty
        - Mention risks, market uncertainty, and limitations.

        You should collaborate with other agents by reviewing and improving their portfolio recommendations with macroeconomic perspectives.

        The final objective is to collectively produce:
        - a well-rounded technology portfolio
        - with justifiable allocation strategies
        - rooted in macroeconomic analysis and evidence
        - while considering risk management and diversification strategies.

        Stay strictly within:
        - investing
        - macroeconomic analysis
        - technology sector analysis
        - finance
        - portfolio management

        Do not provide guaranteed investment advice.
        Always mention uncertainty and risk.
        """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.8

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        portfolio = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            review_message = f"""
            Here is my macroeconomic analysis of our current technology portfolio.

            Please review it from your own financial specialization and improve it.

            You may:
            - challenge my economic assumptions
            - identify missing economic risks
            - suggest sector rotations based on macro trends
            - evaluate the portfolio's sensitivity to interest rate changes
            - recommend allocation changes based on inflation outlook

            Current Analysis and Portfolio Proposal:
            {portfolio}
            """
            response = await self.send_message(messages.Message(content=review_message), recipient)
            portfolio = response.content
        return messages.Message(content=portfolio)