import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LabelList,
} from "recharts";

const cashflowData = [
  { year: "2010", cfo: 32, cfi: -14, cff: 8, net: 26 },
  { year: "2012", cfo: 48, cfi: -20, cff: -6, net: 22 },
  { year: "2014", cfo: 39, cfi: -28, cff: 12, net: 23 },
  { year: "2016", cfo: 45, cfi: -22, cff: 18, net: 36 },
  { year: "2018", cfo: 20, cfi: -30, cff: 2, net: -8 },
  { year: "2020", cfo: 38, cfi: -12, cff: 5, net: 31 },
  { year: "2022", cfo: 44, cfi: -18, cff: 10, net: 36 },
  { year: "2024", cfo: 50, cfi: -23, cff: 16, net: 43 },
];

export default function CashFlowPanel() {
  return (
    <section className="cashflow-panel card card--deep">
      <div className="cashflow-bg-grid" />
      <div className="cashflow-glow cashflow-glow--one" />
      <div className="cashflow-glow cashflow-glow--two" />

      <div className="cashflow-header">
        <div>
          <span className="cashflow-label">Cash flow constellation</span>
          <h2 className="cashflow-title">See cash flow as a flowing map</h2>
          <p className="cashflow-copy">
            Explore CFO, CFI, and Net Cash Flow across the years with layered
            areas and precision labels. This chart reveals the rhythm of long-term
            corporate cash movement.
          </p>
        </div>

        <div className="cashflow-stats">
          <span className="cashflow-pill">CFO CAGR 12.4%</span>
          <span className="cashflow-pill">Net CF 2024: 43%</span>
          <span className="cashflow-pill">CFI trend -18%</span>
        </div>
      </div>

      <div className="cashflow-chart-shell">
        <ResponsiveContainer width="100%" height={360}>
          <AreaChart data={cashflowData} margin={{ top: 12, right: 18, left: 0, bottom: 2 }}>
            <defs>
              <linearGradient id="cfoGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4d8cff" stopOpacity={0.45} />
                <stop offset="95%" stopColor="#4d8cff" stopOpacity={0.08} />
              </linearGradient>
              <linearGradient id="cfiGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ea5fff" stopOpacity={0.45} />
                <stop offset="95%" stopColor="#ea5fff" stopOpacity={0.06} />
              </linearGradient>
              <linearGradient id="netGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ffa74d" stopOpacity={0.34} />
                <stop offset="95%" stopColor="#ffa74d" stopOpacity={0.04} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="rgba(229, 231, 235, 0.08)" strokeDasharray="4 8" />
            <XAxis dataKey="year" tick={{ fill: "#cbd5e1", fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#cbd5e1", fontSize: 12 }} axisLine={false} tickLine={false} unit="%" />
            <Tooltip contentStyle={{ background: "rgba(15, 23, 42, 0.96)", border: "1px solid rgba(148, 163, 184, 0.16)", color: "#f8fafc" }} labelStyle={{ color: "#e2e8f0" }} />
            <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ paddingTop: 10, color: "#e2e8f0" }} />
            <Area
              type="monotone"
              dataKey="cfo"
              stroke="#4d8cff"
              fill="url(#cfoGradient)"
              fillOpacity={1}
              strokeWidth={3}
              dot={{ fill: "#dbeafe", stroke: "#4d8cff", strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6 }}
              name="CFO"
            >
              <LabelList dataKey="cfo" position="top" formatter={(value) => `${value}%`} style={{ fill: "#dbeafe", fontSize: 11, fontWeight: 600 }} />
            </Area>
            <Area
              type="monotone"
              dataKey="cfi"
              stroke="#ea5fff"
              fill="url(#cfiGradient)"
              fillOpacity={1}
              strokeWidth={3}
              dot={{ fill: "#f5d0fe", stroke: "#ea5fff", strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6 }}
              name="CFI"
            >
              <LabelList dataKey="cfi" position="top" formatter={(value) => `${value}%`} style={{ fill: "#f5d0fe", fontSize: 11, fontWeight: 600 }} />
            </Area>
            <Area
              type="monotone"
              dataKey="net"
              stroke="#ffa74d"
              fill="url(#netGradient)"
              fillOpacity={1}
              strokeWidth={3}
              dot={{ fill: "#ffedd5", stroke: "#ffb347", strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6 }}
              name="Net Cash Flow"
            >
              <LabelList dataKey="net" position="top" formatter={(value) => `${value}%`} style={{ fill: "#ffe7c4", fontSize: 11, fontWeight: 600 }} />
            </Area>
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

// In Compare.jsx or CompanyDetail.jsx:
// import CashFlowPanel from "../components/CashFlowPanel";
// ...
// <CashFlowPanel />
