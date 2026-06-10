export default function ConversationInfo({ conversationId }) {
  return (
    <div className="conversation-info">
      <div>
        <span className="eyebrow">AI Chat</span>
        <h2>Tell NutriPlannerAI what diet you want</h2>
      </div>
      <span className="conversation-id">{conversationId}</span>
    </div>
  );
}
