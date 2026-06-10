import Badge from './Badge.jsx';
import SectionTitle from '../common/SectionTitle.jsx';

export default function OptimizationStatusCard({ status }) {
  return (
    <section className="dashboard-card">
      <SectionTitle eyebrow="LP Result" title="Optimization Status" />
      <div className="status-stack">
        {status.badges.map((badge) => (
          <Badge key={badge.label} label={badge.label} type={badge.type} />
        ))}
      </div>
      <p className="status-note">{status.note}</p>
    </section>
  );
}
