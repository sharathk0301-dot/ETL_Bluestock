import { Link } from "react-router-dom";
import HealthBadge from "./HealthBadge";

function CompanyCard({ company }) {
  return (
    <div className="card company-card">
      <h3>{company.name}</h3>
      <p><strong>Symbol:</strong> {company.symbol}</p>
      <p><strong>Sector:</strong> {company.sector}</p>
      <p>
        <strong>Health:</strong> <HealthBadge label={company.health} />
      </p>
      <Link to={`/company/${company.symbol}`} className="view-link">
        View Details
      </Link>
    </div>
  );
}

export default CompanyCard;