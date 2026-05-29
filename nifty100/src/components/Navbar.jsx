import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar__brand">
        <Link to="/">Nifty100</Link>
      </div>

      <nav className="navbar__links">
        <Link to="/companies">Companies</Link>
        <Link to="/compare">Compare</Link>
        <Link to="/screener">Screener</Link>
        <Link to="/sector/IT">Sector View</Link>
      </nav>
    </header>
  );
}
