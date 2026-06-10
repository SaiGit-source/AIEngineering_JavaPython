import MealCard from './MealCard.jsx';
import SectionTitle from '../common/SectionTitle.jsx';

export default function MealTimeline({ meals }) {
  return (
    <section className="meal-timeline-section">
      <SectionTitle eyebrow="Daily Plan" title="Breakfast, Lunch and Dinner" />
      <div className="meal-timeline">
        {meals.map((meal) => (
          <MealCard key={meal.name} meal={meal} />
        ))}
      </div>
    </section>
  );
}
