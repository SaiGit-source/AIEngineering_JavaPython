from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
        You are a specialized financial portfolio analysis agent working within a collaborative multi-agent investment system.

        Your task is to help construct and refine a final technology-focused stock portfolio.

        Depending on your specialization, you may analyze:
        - Market news
        - Earnings
        - Stock fundamentals
        - Technical indicators
        - Risk and diversification
        - Market sentiment
        - Macroeconomic conditions
        - Sector allocation
        - Compliance and risk disclosures

        You should use available tools whenever relevant, including:
        - Web search / Serper
        - Stock quote tools
        - Fundamental analysis tools
        - Historical price tools
        - Portfolio analytics tools

        Your goal is NOT merely to discuss stocks.
        Your goal is to contribute meaningful analysis that helps produce a final recommended portfolio allocation.

        You may:
        - Recommend stocks
        - Reject stocks
        - Suggest allocation percentages
        - Identify portfolio risks
        - Suggest diversification improvements
        - Adjust allocations based on risk or market conditions

        Every response must contain:

        1. Tools Used
        - List tools used and what they were used for.

        2. Evidence Found
        - Summarize important findings from the tools.

        3. Portfolio Recommendations
        - Recommend stocks, sectors, or allocation changes.

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

        You should collaborate with other agents by reviewing and improving their portfolio recommendations.

        The final objective is to collectively produce:
        - a realistic technology portfolio
        - with justified allocation decisions
        - supported by financial evidence and tools
        - while considering risk management and diversification

        Stay strictly within:
        - investing
        - stock market analysis
        - portfolio management
        - finance
        - banking
        - technology-sector investing

        Do not provide guaranteed investment advice.
        Always mention uncertainty and risk.
        """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.8

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

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
        #80% chance this logic works
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient() # find other recipient to bounce idea off of. This is a helper function that finds another agent in the system to send a message to. You can also implement your own logic to find a recipient.
            review_message = f"""
            Here is my current technology portfolio analysis and proposed portfolio allocation.

            Please review it from your own financial specialization and improve it.

            You may:
            - challenge weak assumptions
            - identify missing risks
            - detect concentration or diversification issues
            - identify valuation concerns
            - evaluate macroeconomic exposure
            - suggest better stock selections
            - recommend allocation adjustments
            - improve portfolio balance
            - add missing market signals or sentiment insights

            If appropriate, refine the final portfolio allocation percentages.

            Your response should include:

            1. Tools Used
            2. Evidence Found
            3. Updated Analysis
            4. Portfolio Impact
            5. Recommended Portfolio Changes
            6. Updated Final Portfolio Allocation
            7. Risks and Uncertainty

            Current Analysis and Portfolio Proposal:
            {portfolio}
            """
            # a random recipient is chosen to bounce the idea off of. The recipient will receive the idea and is expected to respond with a refined version of the idea. This is a simple way to simulate collaboration between agents, but you can also implement more complex logic to choose recipients based on their specialties or past interactions.
            # it will take the refined business idea and return it as the final response. This is a simple way to simulate the process of refining ideas through collaboration, but you can also implement more complex logic to combine ideas from multiple agents or to iterate on ideas multiple times.
            response = await self.send_message(messages.Message(content=review_message), recipient)
            portfolio = response.content
            # it either returns its original idea or the refined idea, depending on whether it bounced the idea off of another agent or not based on the probability.
        return messages.Message(content=portfolio)