import { useEffect, useMemo, useState } from "react";
import { fetchCompanies } from "../../api/companies";
import { Link } from "react-router-dom";

export default function Screener() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [minRoe, setMinRoe] = useState(12);
  const [maxDebtEquity, setMaxDebtEquity] = useState(1.5);
  const [sector, setSector] = useState("All Sectors");

  useEffect(() => {
    async function loadCompanies() {
      try {
        const data = await fetchCompanies();
        setCompanies(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message || "Unable to load screener data.");
      } finally {
        setLoading(false);
      }
    }

    loadCompanies();
  }, []);

  const filteredCompanies = useMemo(() => {
    return companies.filter((company) => {
      const roe = Number(company.roe ?? 0);
      const debtEq = Number(company.debt_equity ?? 0);
      const matchesRoe = roe >= Number(minRoe || 0);
      const matchesDebt = debtEq <= Number(maxDebtEquity || 999);
      const matchesSector =
        sector === "All Sectors" || company.sector === sector;
      return matchesRoe && matchesDebt && matchesSector;
    });
  }, [companies, minRoe, maxDebtEquity, sector]);

  const sectors = [
    "All Sectors",
    ...Array.from(new Set(companies.map((company) => company.sector))).sort(),
  ];

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Screening tools</p>
          <h1>Stock Screener</h1>
          <p className="page-subtext">
            Refine the discussion with key filters, then review matching Nifty 100 companies.
          </p>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card card--accent">
          <h2>Filter selections</h2>
          <div className="filter-box">
            <label>Minimum ROE (%)</label>
            <input
              type="number"
              value={minRoe}
              onChange={(e) => setMinRoe(e.target.value)}
              placeholder="e.g., 15"
            />
          </div>

          <div className="filter-box">
            <label>Maximum Debt / Equity</label>
            <input
              type="number"
              value={maxDebtEquity}
              onChange={(e) => setMaxDebtEquity(e.target.value)}
              placeholder="e.g., 0.5"
              step="0.1"
            />
          </div>

          <div className="filter-box">
            <label>Sector</label>
            <select value={sector} onChange={(e) => setSector(e.target.value)}>
              {sectors.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>

          <button className="btn btn--primary btn-wide" onClick={(e) => e.preventDefault()}>
            Apply Filters
          </button>
        </div>

        <div className="card">
          <h2>Preview results</h2>
          {loading ? (
            <p>Loading companies for screening…</p>
          ) : error ? (
            <p className="status-message">{error}</p>
          ) : (
            <>
              <p className="page-subtext">
                {filteredCompanies.length} companies match these criteria. Select a symbol for details.
              </p>
              <div className="result-list">
                {filteredCompanies.slice(0, 8).map((company) => (
                  <Link
                    key={company.symbol}
                    to={`/company/${company.symbol}`}
                    className="result-item"
                  >
                    <div>
                      <strong>{company.symbol}</strong> {company.name}
                    </div>
                    <span>{company.sector}</span>
                  </Link>
                ))}
                {filteredCompanies.length === 0 && (
                  <div className="result-empty">No companies match the current filters.</div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  );
}
