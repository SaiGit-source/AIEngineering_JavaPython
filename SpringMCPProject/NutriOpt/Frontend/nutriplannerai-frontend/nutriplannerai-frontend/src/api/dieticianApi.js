export async function sendDieticianQuestion({ question, conversationId }) {
  const params = new URLSearchParams({ question });

  if (conversationId) {
    params.set('conversationId', conversationId);
  }

  const response = await fetch(`/api/chat?${params.toString()}`);

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.text();
}
