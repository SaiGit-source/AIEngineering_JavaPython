import SectionTitle from '../common/SectionTitle.jsx';
import { formatCurrency } from '../../utils/formatNutrition.js';

export default function CostBreakdownCard({ cost, meals }) {
  return (
    <section className="dashboard-card">
      <SectionTitle eyebrow="Cost" title="Estimated Daily Cost" />
      <div className="cost-total">{formatCurrency(cost.total)}</div>
      <div className="cost-list">
        {meals.map((meal) => (
          <div key={meal.name}>
            <span>{meal.name}</span>
            <strong>{formatCurrency(meal.cost)}</strong>
          </div>
        ))}
      </div>
      {cost.estimated && <p className="muted-note">Some prices use estimated fallback values.</p>}
    </section>
  );
}
