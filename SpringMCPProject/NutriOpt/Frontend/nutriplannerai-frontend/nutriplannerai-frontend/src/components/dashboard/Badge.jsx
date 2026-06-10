export default function Badge({ label, type = 'neutral' }) {
  return <span className={`badge badge-${type}`}>{label}</span>;
}
