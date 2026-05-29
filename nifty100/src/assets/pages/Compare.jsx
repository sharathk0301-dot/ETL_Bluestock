import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { fetchCompanies } from "../../api/companies";
import CashFlowPanel from "../../components/CashFlowPanel";

export default function Compare() {
  const [companies, setCompanies] = useState([]);
  const [selectedSymbols, setSelectedSymbols] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCompanies() {
      try {
        const data = await fetchCompanies();
        setCompanies(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Failed to load companies:", err);
      } finally {
        setLoading(false);
      }
    }

    loadCompanies();
  }, []);

  const selectedCompanies = useMemo(
    () => companies.filter((company) => selectedSymbols.includes(company.symbol)),
    [companies, selectedSymbols]
  );

  function toggleSelection(symbol) {
    setSelectedSymbols((current) => {
      if (current.includes(symbol)) {
        return current.filter((item) => item !== symbol);
      }
      if (current.length >= 2) {
        return [current[1], symbol];
      }
      return [...current, symbol];
    });
  }

  function formatMetric(value, suffix = "%") {
    return value == null ? "N/A" : `${value}${suffix}`;
  }

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Analysis center</p>
          <h1>Compare Companies</h1>
          <p className="page-subtext">
            Build side-by-side comparisons of Nifty 100 companies and review core financial signals.
          </p>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card card--accent">
          <h2>Comparison workflow</h2>
          <p>
            Click cards to add companies to the compare panel, then use the summary cards below to review
            relative strength in ROE, Debt/Equity, and operating margin.
          </p>
        </div>

        <div className="card card--accent">
          <h2>Why compare?</h2>
          <ul className="feature-list">
            <li>Confirm sector strength before you invest.</li>
            <li>Spot relative valuation differences quickly.</li>
            <li>Use metrics to identify long-term leaders.</li>
          </ul>
        </div>
      </div>

      <section className="compare-select-panel">
        <div className="compare-select-header">
          <div>
            <h2>Select up to two companies</h2>
            <p className="page-subtext">
              Tap a card to save it for comparison. Selected companies are highlighted and shown in the summary below.
            </p>
          </div>
          <div className="compare-status">
            <span>
              {loading ? "Loading companies..." : selectedCompanies.length === 0 ? "Choose one company to begin." : selectedCompanies.length === 1 ? "Pick one more company to compare." : "Ready to compare."}
            </span>
            {selectedCompanies.length > 0 && (
              <span>
                Selected: {selectedCompanies.map((company) => company.symbol).join(" / ")}
              </span>
            )}
          </div>
        </div>

        <div className="company-grid">
          {loading
            ? Array.from({ length: 6 }).map((_, index) => (
                <div key={index} className="company-card company-card--placeholder">
                  <div className="company-card__top">
                    <h3>Loading...</h3>
                  </div>
                </div>
              ))
            : companies.map((company) => {
                const isActive = selectedSymbols.includes(company.symbol);
                return (
                  <div
                    key={company.symbol}
                    className={`company-card company-card--selectable ${isActive ? "company-card--selected" : ""}`}
                    onClick={() => toggleSelection(company.symbol)}
                  >
                    <div className="company-card__top">
                      <div>
                        <h3>{company.name}</h3>
                        <p className="company-symbol">{company.symbol}</p>
                      </div>
                      <span className="company-arrow">{isActive ? "✓" : "→"}</span>
                    </div>

                    <div className="company-meta">
                      <div>
                        <span className="meta-label">Sector</span>
                        <span className="meta-value">{company.sector || "—"}</span>
                      </div>
                      <div>
                        <span className="meta-label">ROE</span>
                        <span className="meta-value">{formatMetric(company.roe)}</span>
                      </div>
                      <div>
                        <span className="meta-label">Debt/Equity</span>
                        <span className="meta-value">{company.debt_equity ?? "N/A"}</span>
                      </div>
                    </div>

                    <div className="company-card__footer">
                      <Link to={`/company/${company.symbol}`} onClick={(event) => event.stopPropagation()}>
                        View profile
                      </Link>
                      <span className="meta-value">{company.health_label?.toUpperCase() || "N/A"}</span>
                    </div>
                  </div>
                );
              })}
        </div>
      </section>

      <CashFlowPanel />

      <div className="compare-grid">
        <div className="card card--floating">
          <h3>Selected companies</h3>
          {selectedCompanies.length === 0 ? (
            <p className="page-subtext">Choose one or two companies above to reveal live comparison metrics.</p>
          ) : (
            selectedCompanies.map((company) => (
              <div key={company.symbol} className="detail-block">
                <h4>{company.name}</h4>
                <div className="detail-row">
                  <span>ROE</span>
                  <strong>{formatMetric(company.roe)}</strong>
                </div>
                <div className="detail-row">
                  <span>Debt / Equity</span>
                  <strong>{company.debt_equity ?? "N/A"}</strong>
                </div>
                <div className="detail-row">
                  <span>Operating margin</span>
                  <strong>{formatMetric(company.opm)}</strong>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="card card--floating">
          <h3>Comparison insight</h3>
          {selectedCompanies.length < 2 ? (
            <p className="page-subtext">Select two companies to compare direct differences across the key metrics.</p>
          ) : (
            <>
              <div className="detail-row">
                <span>ROE gap</span>
                <strong>{Math.abs((selectedCompanies[0].roe || 0) - (selectedCompanies[1].roe || 0)).toFixed(1)}%</strong>
              </div>
              <div className="detail-row">
                <span>Debt/Equity gap</span>
                <strong>{Math.abs((selectedCompanies[0].debt_equity || 0) - (selectedCompanies[1].debt_equity || 0)).toFixed(2)}</strong>
              </div>
              <div className="detail-row">
                <span>Operating margin gap</span>
                <strong>{Math.abs((selectedCompanies[0].opm || 0) - (selectedCompanies[1].opm || 0)).toFixed(1)}%</strong>
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  );
}


