import MacroProgressBar from './MacroProgressBar.jsx';
import SectionTitle from '../common/SectionTitle.jsx';

export default function MacroProgressPanel({ totals, targets }) {
  const rows = [
    { label: 'Calories', value: totals.calories, target: targets.calories, unit: 'kcal' },
    { label: 'Protein', value: totals.protein, target: targets.protein, unit: 'g' },
    { label: 'Carbs', value: totals.carbs, target: targets.carbs, unit: 'g' },
    { label: 'Fat', value: totals.fat, target: targets.fat, unit: 'g' },
    { label: 'Fiber', value: totals.fiber, target: targets.fiber, unit: 'g' }
  ];

  return (
    <section className="dashboard-card">
      <SectionTitle eyebrow="Targets" title="Macro Progress" />
      <div className="macro-progress-list">
        {rows.map((row) => (
          <MacroProgressBar key={row.label} {...row} />
        ))}
      </div>
    </section>
  );
}
