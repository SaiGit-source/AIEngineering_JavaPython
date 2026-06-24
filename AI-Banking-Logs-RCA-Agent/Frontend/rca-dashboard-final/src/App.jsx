import { useEffect, useState } from "react";
import AiRcaPanel from "./components/AiRcaPanel";
import ChartsSection from "./components/ChartsSection";
import KpiCards from "./components/KpiCards";
import TraceTable from "./components/TraceTable";
import { fetchDashboardOverview } from "./api";

const emptyOverview = {
  errorCodes: [],
  errorsByService: [],
  errorTrend: [],
  traces: []
};

export default function App() {
  const [overview, setOverview] = useState(emptyOverview);
  const [selectedTrace, setSelectedTrace] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dashboardError, setDashboardError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await fetchDashboardOverview();
        setOverview(data);
        setSelectedTrace(data.traces?.[0] || null);
      } catch (err) {
        setDashboardError(err.message || "Failed to load dashboard overview");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI-Banking-Logs-RCA-Agent</p>
          <h1>Banking RCA Dashboard MVP</h1>
          <p className="subtitle">
            Charts from Spring Boot raw log aggregation. RCA from Pinecone RAG + ChatClient.
          </p>
        </div>
        <div className="env-pill">simulated-prod</div>
      </header>

      {loading && <div className="info-box">Loading dashboard data from Spring Boot...</div>}

      {dashboardError && (
        <div className="error-box">
          Could not load dashboard data. Make sure Spring Boot is running on http://localhost:8080.
          <br />
          {dashboardError}
        </div>
      )}

      {!loading && !dashboardError && (
        <main>
          <KpiCards overview={overview} />
          <ChartsSection overview={overview} />

          <div className="main-grid">
            <div className="left-column">
              <TraceTable
                traces={overview.traces}
                selectedTrace={selectedTrace}
                onSelectTrace={setSelectedTrace}
              />
            </div>

            <div className="right-column">
              <AiRcaPanel selectedTrace={selectedTrace} />
            </div>
          </div>
        </main>
      )}
    </div>
  );
}
