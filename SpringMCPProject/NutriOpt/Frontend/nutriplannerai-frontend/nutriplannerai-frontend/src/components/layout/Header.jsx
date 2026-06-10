export default function Header() {
  return (
    <header className="app-header">
      <div>
        <h1>NutriPlannerAI</h1>
        <p>AI Meal Planning + Diet Optimization</p>
      </div>
      <div className="header-status">
        <span className="status-dot" />
        Dashboard Preview
      </div>
    </header>
  );
}
