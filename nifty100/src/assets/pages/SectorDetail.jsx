import { useEffect, useMemo, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchCompanies } from "../../api/companies";

export default function SectorDetail() {
  const { name } = useParams();
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCompanies() {
      try {
        const data = await fetchCompanies();
        setCompanies(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message || "Unable to load sector data.");
      } finally {
        setLoading(false);
      }
    }

    loadCompanies();
  }, []);

  const sectorName = name || "IT";
  const filteredCompanies = useMemo(
    () =>
      companies.filter(
        (company) =>
          company.sector?.toLowerCase() === sectorName.toLowerCase()
      ),
    [companies, sectorName]
  );

  const topCompanies = useMemo(
    () =>
      filteredCompanies
        .slice()
        .sort((a, b) => (b.roe ?? 0) - (a.roe ?? 0))
        .slice(0, 5),
    [filteredCompanies]
  );

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Sector focus</p>
          <h1>{sectorName} Sector</h1>
          <p className="page-subtext">
            View companies and sector insights for {sectorName}. This page is ready for drill-down data.
          </p>
        </div>

        <Link to="/companies" className="btn btn--secondary">
          Browse Companies
        </Link>
      </div>

      {loading ? (
        <div className="status-card">Loading sector companies…</div>
      ) : error ? (
        <div className="status-card">Error: {error}</div>
      ) : (
        <div className="grid grid-2">
          <div className="card">
            <h2>Sector overview</h2>
            <p>
              Companies in {sectorName} can be compared across revenue, margins, and balance sheet strength.
              Use the company page to drill into specific symbols.
            </p>
          </div>

          <div className="card">
            <h2>Top companies</h2>
            {topCompanies.length ? (
              <ul className="feature-list">
                {topCompanies.map((company) => (
                  <li key={company.symbol}>
                    <Link to={`/company/${company.symbol}`} className="view-link">
                      {company.name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No companies found for this sector.</p>
            )}
          </div>
        </div>
      )}
    </main>
  );
}
