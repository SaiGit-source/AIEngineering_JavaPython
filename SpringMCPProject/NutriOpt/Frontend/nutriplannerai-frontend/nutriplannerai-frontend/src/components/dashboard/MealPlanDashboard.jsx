import DashboardSummaryCard from './DashboardSummaryCard.jsx';
import MealTimeline from './MealTimeline.jsx';
import MacroProgressPanel from './MacroProgressPanel.jsx';
import MacroDonutChart from './MacroDonutChart.jsx';
import CostBreakdownCard from './CostBreakdownCard.jsx';
import OptimizationStatusCard from './OptimizationStatusCard.jsx';

export default function MealPlanDashboard({ mealPlan }) {
  return (
    <div className="dashboard-pane pane-card">
      <DashboardSummaryCard mealPlan={mealPlan} />

      <div className="dashboard-grid">
        <div className="dashboard-main-column">
          <MealTimeline meals={mealPlan.meals} />
        </div>
        <div className="dashboard-side-column">
          <MacroProgressPanel totals={mealPlan.totals} targets={mealPlan.targets} />
          <MacroDonutChart macros={mealPlan.macroDistribution} />
          <CostBreakdownCard cost={mealPlan.cost} meals={mealPlan.meals} />
          <OptimizationStatusCard status={mealPlan.optimization} />
        </div>
      </div>
    </div>
  );
}
