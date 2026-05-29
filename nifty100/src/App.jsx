import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./assets/pages/Home";
import Companies from "./assets/pages/Companies";
import CompanyDetail from "./assets/pages/CompanyDetail";
import Compare from "./assets/pages/Compare";
import Screener from "./assets/pages/Screener";
import SectorDetail from "./assets/pages/SectorDetail";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/company/:symbol" element={<CompanyDetail />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/screener" element={<Screener />} />
            <Route path="/sector/:name" element={<SectorDetail />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </BrowserRouter>
  );
}
