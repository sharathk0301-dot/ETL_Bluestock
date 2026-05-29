import { Link } from "react-router-dom";
import { useEffect } from "react";
import Map3DCard from "../../components/Map3DCard";

const cards = [
  {
    title: "Companies",
    description:
      "Browse Nifty 100 companies with a cleaner overview and quicker navigation.",
    to: "/companies",
  },
  {
    title: "Compare",
    description: "Compare company fundamentals and key metrics side by side.",
    to: "/compare",
  },
  {
    title: "Screener",
    description:
      "Apply filters and find stocks that match your investing criteria.",
    to: "/screener",
  },
  {
    title: "Sector View",
    description:
      "Explore sector-level grouping and drill down into sector pages.",
    to: "/sector/IT",
  },
];

export default function Home() {
  // Fade‑in on scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.18 }
    );

    document
      .querySelectorAll(".reveal-on-scroll")
      .forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  return (
    <main className="home">
      {/* HERO */}
      
      <section className="hero hero--glow reveal-on-scroll">
        <div className="hero-overlay" />
        <div className="hero__light-orbit" />
        <div className="hero__grid" />

        <div className="hero-inner">
          <div className="hero-copy">
            <span className="hero__badge">Market Intelligence Dashboard</span>

            <h1>Track, compare, and explore Nifty 100 stocks in one place</h1>

            <p>
              A modern stock dashboard for browsing companies, comparing
              performance, filtering ideas, and navigating sectors with a cleaner
              user experience.
            </p>

            <div className="hero__actions">
              <Link to="/companies" className="btn btn--primary">
                Explore Companies
              </Link>
              <Link to="/compare" className="btn btn--secondary">
                Start Comparing
              </Link>
            </div>
          </div>

          <div className="hero__stats">
            <div className="stat-box stat-box--3d">
              <div className="stat-box__glare" />
              <h3>100+</h3>
              <p>Nifty companies</p>
            </div>
            <div className="stat-box stat-box--3d">
              <div className="stat-box__glare" />
              <h3>4</h3>
              <p>Core dashboards</p>
            </div>
            <div className="stat-box stat-box--3d">
              <div className="stat-box__glare" />
              <h3>Fast</h3>
              <p>Insight-ready data</p>
            </div>
          </div>
        </div>
      </section>

      {/* OVERVIEW + FEATURE GRID */}
      <section className="home__overview reveal-on-scroll">
        <div className="overview-intro">
          <h2 className="section-title">Professional insights, simplified</h2>
          <p className="section-copy">
            Quickly access company fundamentals, compare sector leaders, and
            apply filters that uncover strong stock ideas. Every page is built
            for confident investing decisions.
          </p>
        </div>

        <div className="feature-grid feature-grid--3d">
          {cards.map((card) => (
            <Link
              to={card.to}
              className="feature-card feature-card--3d"
              key={card.title}
            >
              <div className="feature-card__inner">
                <div className="feature-card__light" />
                <div className="feature-card__top">
                  <h3>{card.title}</h3>
                  <span className="feature-card__arrow">→</span>
                </div>
                <p>{card.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="home__orbit reveal-on-scroll">
        <Map3DCard />
      </section>
    </main>
  );
}