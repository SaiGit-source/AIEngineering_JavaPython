export default function SectionTitle({ eyebrow, title }) {
  return (
    <div className="section-title">
      {eyebrow && <span>{eyebrow}</span>}
      <h3>{title}</h3>
    </div>
  );
}
