from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
from dotenv import load_dotenv

load_dotenv(override=True)

class ReportEvaluatorAgent(RoutedAgent):

    system_message = """
    You are a Senior Portfolio Evaluation Agent.

    Your job is to review multiple portfolio analyses created by other financial agents
    and produce one consolidated technology portfolio report.

    You must evaluate:
    - tools used by each agent
    - evidence quality
    - stock selections
    - allocation logic
    - concentration risk
    - diversification
    - valuation concerns
    - market/news signals
    - conflicting opinions between agents

    Your final report must include:

    1. Executive Summary
    2. Tools and Evidence Reviewed
    3. Common Findings Across Agents
    4. Conflicting Opinions
    5. Final Recommended Technology Portfolio
    6. Allocation Percentages
    7. Reasoning Behind Allocation
    8. Key Risks
    9. Simple Explanation
    10. Final Disclaimer

    Do not provide guaranteed investment advice.
    Mention uncertainty and market risk.
    """

    def __init__(self, name) -> None:
        super().__init__(name)

        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            temperature=0.3
        )

        self._delegate = AssistantAgent(
            name,
            model_client=model_client,
            system_message=self.system_message
        )

    @message_handler
    async def handle_message(
        self,
        message: messages.Message,
        ctx: MessageContext
    ) -> messages.Message:

        text_message = TextMessage(
            content=message.content,
            source="user"
        )

        response = await self._delegate.on_messages(
            [text_message],
            ctx.cancellation_token
        )

        return messages.Message(content=response.chat_message.content)