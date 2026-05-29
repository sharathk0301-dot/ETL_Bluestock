import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { fetchCompanies } from "../../api/companies";

export default function Companies() {
  const [companies, setCompanies] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCompanies() {
      try {
        const data = await fetchCompanies();
        setCompanies(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message || "Unable to load companies");
      } finally {
        setLoading(false);
      }
    }

    loadCompanies();
  }, []);

  const filteredCompanies = useMemo(() => {
    const term = search.toLowerCase().trim();

    if (!term) return companies;

    return companies.filter((company) => {
      const name = company.name?.toLowerCase() || "";
      const symbol = company.symbol?.toLowerCase() || "";
      const sector = company.sector?.toLowerCase() || "";
      return (
        name.includes(term) ||
        symbol.includes(term) ||
        sector.includes(term)
      );
    });
  }, [companies, search]);

  if (loading) {
    return <div className="page"><h2>Loading companies...</h2></div>;
  }

  if (error) {
    return <div className="page"><h2>{error}</h2></div>;
  }

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Market Directory</p>
          <h1>Companies</h1>
          <p className="page-subtext">
            Search and explore Nifty 100 companies by name, symbol, or sector.
          </p>
        </div>
      </div>

      <div className="toolbar">
        <input
          type="text"
          placeholder="Search by company, symbol, or sector"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
        <div className="results-chip">
          {filteredCompanies.length} Results
        </div>
      </div>

      <div className="company-grid">
        {filteredCompanies.map((company) => (
          <Link
            key={company.symbol}
            to={`/company/${company.symbol}`}
            className="company-card"
          >
            <div className="company-card__top">
              <div>
                <h3>{company.name || "Unknown Company"}</h3>
                <p className="company-symbol">{company.symbol || "--"}</p>
              </div>
              <span className="company-arrow">→</span>
            </div>

            <div className="company-meta">
              <div>
                <span className="meta-label">Sector</span>
                <span className="meta-value">{company.sector || "N/A"}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}