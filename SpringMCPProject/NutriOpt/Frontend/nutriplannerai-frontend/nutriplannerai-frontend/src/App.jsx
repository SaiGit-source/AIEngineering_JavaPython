import Header from './components/layout/Header.jsx';
import TwoPaneLayout from './components/layout/TwoPaneLayout.jsx';
import ChatPane from './components/chat/ChatPane.jsx';
import MealPlanDashboard from './components/dashboard/MealPlanDashboard.jsx';
import { useDieticianChat } from './hooks/useDieticianChat.js';
import { sampleMealPlan } from './data/sampleMealPlan.js';

export default function App() {
  const {
    conversationId,
    messages,
    mealPlan,
    loading,
    error,
    sendMessage
  } = useDieticianChat(sampleMealPlan);

  return (
    <div className="app-shell">
      <Header />
      <TwoPaneLayout
        left={
          <ChatPane
            conversationId={conversationId}
            messages={messages}
            loading={loading}
            error={error}
            onSendMessage={sendMessage}
          />
        }
        right={<MealPlanDashboard mealPlan={mealPlan} />}
      />
    </div>
  );
}
