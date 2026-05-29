import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import HealthBadge from "../../components/HealthBadge";
import { fetchCompanyDetail } from "../../api/companies";

export default function CompanyDetail() {
  const { symbol } = useParams();
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCompany() {
      try {
        const data = await fetchCompanyDetail(symbol);
        setCompany(data);
      } catch (err) {
        setError(err.message || "Unable to load company details.");
      } finally {
        setLoading(false);
      }
    }

    loadCompany();
  }, [symbol]);

  if (loading) {
    return (
      <main className="page">
        <div className="status-card">Loading company details...</div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="page">
        <div className="status-card">Error: {error}</div>
      </main>
    );
  }

  if (!company) {
    return (
      <main className="page">
        <div className="status-card">No company found.</div>
      </main>
    );
  }

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Company profile</p>
          <h1>{company.name || "Company"}</h1>
          <p className="page-subtext">
            Details for {company.symbol || "the selected company"} from the Nifty 100 list.
          </p>
        </div>
        <Link to="/companies" className="btn btn--secondary">
          Back to Companies
        </Link>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h2>Overview</h2>
          <div className="detail-row">
            <span>Symbol</span>
            <strong>{company.symbol || "—"}</strong>
          </div>
          <div className="detail-row">
            <span>Sector</span>
            <strong>{company.sector || "—"}</strong>
          </div>
          <div className="detail-row">
            <span>Health Score</span>
            <strong>{company.health_score ?? "N/A"}</strong>
          </div>
          <div className="detail-row">
            <span>Status</span>
            <HealthBadge label={company.health_label || "Average"} />
          </div>
        </div>

        <div className="card">
          <h2>Company insights</h2>
          <p>
            {company.description ||
              "Key company metrics and sector insights are available through the Django API."}
          </p>
          <div className="metric-grid">
            <div className="metric-card">
              <span>ROE</span>
              <strong>{company.roe ?? "N/A"}%</strong>
            </div>
            <div className="metric-card">
              <span>Debt / Equity</span>
              <strong>{company.debt_equity ?? "N/A"}</strong>
            </div>
            <div className="metric-card">
              <span>Operating Margin</span>
              <strong>{company.opm ?? "N/A"}%</strong>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
