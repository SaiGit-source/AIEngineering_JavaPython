export default function Pane({ title, children }) {
  return (
    <div className="pane-card">
      {title && <h2>{title}</h2>}
      {children}
    </div>
  );
}
