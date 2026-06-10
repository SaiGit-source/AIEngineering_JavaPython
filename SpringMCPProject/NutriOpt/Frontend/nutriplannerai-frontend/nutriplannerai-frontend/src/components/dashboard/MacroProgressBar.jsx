import { formatNumber } from '../../utils/formatNutrition.js';

export default function MacroProgressBar({ label, value, target, unit }) {
  const percentage = target > 0 ? Math.min((value / target) * 100, 115) : 0;

  return (
    <div className="macro-progress-row">
      <div className="macro-progress-label">
        <span>{label}</span>
        <strong>{formatNumber(value)} / {formatNumber(target)} {unit}</strong>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}
