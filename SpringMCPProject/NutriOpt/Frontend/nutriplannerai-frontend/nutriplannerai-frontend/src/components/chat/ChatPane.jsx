import { useState } from 'react';
import ConversationInfo from './ConversationInfo.jsx';
import ChatMessage from './ChatMessage.jsx';
import PromptInput from './PromptInput.jsx';
import LoadingSpinner from '../common/LoadingSpinner.jsx';
import ErrorMessage from '../common/ErrorMessage.jsx';

export default function ChatPane({ conversationId, messages, loading, error, onSendMessage }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = () => {
    const trimmedPrompt = prompt.trim();
    if (!trimmedPrompt || loading) return;
    onSendMessage(trimmedPrompt);
    setPrompt('');
  };

  return (
    <div className="chat-pane pane-card">
      <ConversationInfo conversationId={conversationId} />

      <div className="chat-messages" aria-live="polite">
        {messages.map((message) => (
          <ChatMessage key={message.id} role={message.role} content={message.content} />
        ))}
        {loading && <LoadingSpinner label="NutriPlannerAI is preparing your plan..." />}
        {error && <ErrorMessage message={error} />}
      </div>

      <PromptInput
        value={prompt}
        onChange={setPrompt}
        onSubmit={handleSubmit}
        disabled={loading}
      />
    </div>
  );
}
