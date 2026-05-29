import { useRef, useState } from "react";

const initialTransform = "perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)";

export default function Map3DCard() {
  const cardRef = useRef(null);
  const [cardTransform, setCardTransform] = useState(initialTransform);

  const handleMouseMove = (event) => {
    const card = cardRef.current;
    if (!card) return;

    const rect = card.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const moveX = (x / rect.width - 0.5) * 26;
    const moveY = (y / rect.height - 0.5) * 20;
    const rotateY = moveX;
    const rotateX = -moveY;

    setCardTransform(
      `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.04)`
    );
  };

  const handleMouseLeave = () => {
    setCardTransform(initialTransform);
  };

  return (
    <div
      ref={cardRef}
      className="card card--3d-map"
      style={{ transform: cardTransform }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      <div className="map3d-bg">
        <div className="map3d-grid" />
        <div className="map3d-star map3d-star--one" />
        <div className="map3d-star map3d-star--two" />
        <div className="map3d-star map3d-star--three" />
        <div className="map3d-star map3d-star--four" />
        <div className="map3d-glow map3d-glow--one" />
        <div className="map3d-glow map3d-glow--two" />
        <div className="map3d-nucleus">
          <div className="map3d-nucleus-core" />
          <div className="map3d-nucleus-ring" />
        </div>

        <div className="map3d-chart map3d-chart--one">
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
        </div>
        <div className="map3d-chart map3d-chart--two">
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
        </div>
        <div className="map3d-chart map3d-chart--three">
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
          <div className="map3d-chart-node" />
        </div>

        <div className="map3d-orbit map3d-orbit--one">
          <div className="node node--sm" />
        </div>
        <div className="map3d-orbit map3d-orbit--two">
          <div className="node node--md" />
        </div>
        <div className="map3d-orbit map3d-orbit--three">
          <div className="node node--lg" />
        </div>

        <div className="map3d-cluster map3d-cluster--a">
          <div className="node node--md" />
          <div className="node node--sm" />
          <div className="node node--sm" />
          <div className="node node--lg" />
        </div>
        <div className="map3d-cluster map3d-cluster--b">
          <div className="node node--sm" />
          <div className="node node--md" />
          <div className="node node--sm" />
        </div>
        <div className="map3d-cluster map3d-cluster--c">
          <div className="node node--lg" />
          <div className="node node--md" />
          <div className="node node--sm" />
        </div>
      </div>

      <div className="map3d-content">
        <span className="map3d-badge">Interactive 3D view</span>
        <h2>See the market as a 3D map</h2>
        <p>
          Visualize Nifty 100 companies as an interactive constellation. Each sector becomes a cluster,
          and each company a moving node sized by market cap.
        </p>
        <span className="map3d-coming">Experimental 3D view coming soon</span>
      </div>
    </div>
  );
}
