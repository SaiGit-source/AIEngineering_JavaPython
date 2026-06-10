export default function LoadingSpinner({ label = 'Loading...' }) {
  return (
    <div className="loading-row">
      <span className="spinner" />
      <span>{label}</span>
    </div>
  );
}
