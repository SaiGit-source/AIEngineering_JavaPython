import { useMemo, useState } from 'react';
import { sendDieticianQuestion } from '../api/dieticianApi.js';
import { parseMealPlanFromText } from '../utils/parseMealPlan.js';

const initialAssistantMessage = {
  id: 'assistant-welcome',
  role: 'assistant',
  content: 'Welcome to NutriPlannerAI. Ask for a diet plan and I will show the full AI response here, while the dashboard displays the breakfast, lunch and dinner plan.'
};

function createConversationId() {
  return `veg-${Math.floor(Math.random() * 9000) + 1000}`;
}

function extractConversationId(responseText, fallbackId) {
  const match = responseText.match(/Conversation ID:\s*([^\n]+)/i);
  return match?.[1]?.trim() || fallbackId;
}

export function useDieticianChat(initialMealPlan) {
  const [conversationId, setConversationId] = useState(createConversationId);
  const [messages, setMessages] = useState([initialAssistantMessage]);
  const [mealPlan, setMealPlan] = useState(initialMealPlan);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendMessage = async (question) => {
    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: question
    };

    setMessages((current) => [...current, userMessage]);
    setLoading(true);
    setError('');

    try {
      const responseText = await sendDieticianQuestion({ question, conversationId });
      const nextConversationId = extractConversationId(responseText, conversationId);
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: responseText
      };

      setConversationId(nextConversationId);
      setMessages((current) => [...current, assistantMessage]);
      setMealPlan(parseMealPlanFromText(responseText));
    } catch (requestError) {
      setError(requestError.message || 'Unable to reach NutriPlannerAI backend.');
    } finally {
      setLoading(false);
    }
  };

  return useMemo(
    () => ({
      conversationId,
      messages,
      mealPlan,
      loading,
      error,
      sendMessage
    }),
    [conversationId, messages, mealPlan, loading, error]
  );
}
