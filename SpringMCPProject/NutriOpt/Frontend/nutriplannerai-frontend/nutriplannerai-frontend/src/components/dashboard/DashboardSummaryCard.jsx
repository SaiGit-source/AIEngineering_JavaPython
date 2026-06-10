import Badge from './Badge.jsx';
import { formatCurrency, formatNumber } from '../../utils/formatNutrition.js';

export default function DashboardSummaryCard({ mealPlan }) {
  return (
    <section className="summary-card">
      <div>
        <span className="eyebrow">Meal Plan Dashboard</span>
        <h2>Today’s Optimized Meal Plan</h2>
        <div className="summary-metrics">
          <strong>{formatNumber(mealPlan.totals.calories)} kcal</strong>
          <strong>{formatNumber(mealPlan.totals.protein)}g protein</strong>
          <strong>{formatCurrency(mealPlan.cost.total)}</strong>
        </div>
      </div>
      <div className="summary-badges">
        {mealPlan.badges.map((badge) => (
          <Badge key={badge.label} label={badge.label} type={badge.type} />
        ))}
      </div>
    </section>
  );
}
