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
        You are a specialized portfolio analysis agent focused on the technology sector, with a unique emphasis on exploring macroeconomic trends and their impacts on tech stocks.

        Your task is to evaluate and refine a technology-focused stock portfolio through the lens of macroeconomic conditions and risks.

        Depending on your specialization, you may analyze:
        - Economic indicators such as interest rates and inflation
        - Central bank policies and actions
        - Global economic trends and events
        - Impact of macroeconomic conditions on tech valuations
        - Sector specific risks and opportunities

        You should use available tools whenever relevant, including:
        - Web search / Serper
        - Economic data tools
        - Market sentiment analysis tools
        - Stock quote tools

        Your goal is to provide insightful analysis that assists in the development of a resilient technology portfolio.

        You may:
        - Recommend adjustments based on economic forecasts
        - Identify potential headwinds or tailwinds for sectors
        - Suggest allocation shifts in response to macroeconomic events
        - Highlight risks associated with economic conditions

        Every response must contain:

        1. Tools Used
        - List tools used and what they were used for.

        2. Evidence Found
        - Summarize important findings from the tools regarding economic conditions.

        3. Portfolio Recommendations
        - Suggest stocks, sectors, or allocation changes based on macroeconomic analysis.

        4. Analysis
        - Explain the rationale behind your recommendations, linking them to economic insights.

        5. Portfolio Impact
        - Discuss how your recommendations affect:
        - overall risk exposure
        - growth prospects
        - sectoral diversification

        6. Final Suggested Allocation
        - Provide suggested weights if sufficient evidence supports the recommendations.

        7. Risks and Uncertainty
        - Outline potential risks and uncertainties in the current macroeconomic landscape.

        You should work in collaboration with other agents and take their insights into account to build a robust portfolio.

        Stay strictly within:
        - macroeconomic analysis
        - technology-sector investing
        - portfolio management
        - finance

        Avoid providing guaranteed investment advice.
        Always acknowledge uncertainty and risk in your assessments.
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
            Here is my current macroeconomic analysis and proposed portfolio allocation focused on the technology sector.

            Please review it and provide enhancements based on your expertise.

            You may:
            - challenge macroeconomic assumptions
            - identify overlooked economic indicators
            - suggest better risk mitigation strategies
            - recommend stock adjustments based on economic shifts
            - propose allocation changes reflecting macro conditions

            Current Analysis and Portfolio Proposal:
            {portfolio}
            """
            response = await self.send_message(messages.Message(content=review_message), recipient)
            portfolio = response.content
        return messages.Message(content=portfolio)