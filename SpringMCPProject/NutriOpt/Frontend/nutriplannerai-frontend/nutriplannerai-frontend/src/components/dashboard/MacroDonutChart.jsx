import SectionTitle from '../common/SectionTitle.jsx';

export default function MacroDonutChart({ macros }) {
  const carbs = macros.carbs;
  const protein = macros.protein;
  const fat = macros.fat;
  const carbsEnd = carbs;
  const proteinEnd = carbs + protein;

  const chartStyle = {
    background: `conic-gradient(#2b7cff 0 ${carbsEnd}%, #28c76f ${carbsEnd}% ${proteinEnd}%, #ffb020 ${proteinEnd}% 100%)`
  };

  return (
    <section className="dashboard-card">
      <SectionTitle eyebrow="Balance" title="Macro Distribution" />
      <div className="donut-chart-row">
        <div className="donut-chart" style={chartStyle}>
          <div className="donut-hole">Macros</div>
        </div>
        <div className="donut-legend">
          <span><i className="legend-dot carbs" />Carbs {macros.carbs}%</span>
          <span><i className="legend-dot protein" />Protein {macros.protein}%</span>
          <span><i className="legend-dot fat" />Fat {macros.fat}%</span>
        </div>
      </div>
    </section>
  );
}
