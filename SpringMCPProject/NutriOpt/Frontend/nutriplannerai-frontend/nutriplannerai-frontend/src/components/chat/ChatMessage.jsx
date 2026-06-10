export default function ChatMessage({ role, content }) {
  const isUser = role === 'user';

  return (
    <article className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-label">{isUser ? 'You' : 'NutriPlannerAI'}</div>
      <p>{content}</p>
    </article>
  );
}
