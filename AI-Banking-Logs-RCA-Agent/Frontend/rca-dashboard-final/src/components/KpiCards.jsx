export default function KpiCards({ overview }) {
  const errorCount = (overview.errorCodes || []).reduce((sum, row) => sum + Number(row.count || 0), 0);
  const serviceCount = overview.errorsByService?.length || 0;
  const traceCount = overview.traces?.length || 0;

  const cards = [
    { label: "Total error signals", value: errorCount },
    { label: "Impacted services", value: serviceCount },
    { label: "Affected traces", value: traceCount },
    { label: "Environment", value: "simulated-prod" }
  ];

  return (
    <div className="kpi-grid">
      {cards.map((item) => (
        <div className="kpi-card" key={item.label}>
          <p>{item.label}</p>
          <strong>{item.value}</strong>
        </div>
      ))}
    </div>
  );
}
