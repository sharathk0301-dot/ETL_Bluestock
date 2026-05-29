function HealthBadge({ label }) {
  const normalized = label?.toLowerCase() || "average";

  return <span className={`badge ${normalized}`}>{label}</span>;
}

export default HealthBadge;