import FoodItemRow from './FoodItemRow.jsx';
import { formatCurrency, formatNumber } from '../../utils/formatNutrition.js';

export default function MealCard({ meal }) {
  return (
    <article className="meal-card">
      <div className="meal-icon" aria-hidden="true">{meal.icon}</div>
      <div className="meal-content">
        <div className="meal-card-header">
          <div>
            <h3>{meal.name}</h3>
            <p>{meal.description}</p>
          </div>
          <span>{formatNumber(meal.calories)} kcal</span>
        </div>

        <div className="food-list">
          {meal.items.map((item) => (
            <FoodItemRow key={`${meal.name}-${item.food}`} item={item} />
          ))}
        </div>

        <div className="meal-footer">
          <span>{formatNumber(meal.protein)}g protein</span>
          <span>{formatCurrency(meal.cost)}</span>
        </div>
      </div>
    </article>
  );
}
