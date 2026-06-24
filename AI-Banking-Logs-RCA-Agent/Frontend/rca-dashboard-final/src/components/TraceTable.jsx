import Card from "./Card";

export default function TraceTable({ traces = [], selectedTrace, onSelectTrace }) {
  return (
    <Card title="Affected traces" subtitle="Select a trace, then ask AI for RCA">
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Trace ID</th>
              <th>Transaction</th>
              <th>Services</th>
              <th>Error codes</th>
              <th>Severity</th>
            </tr>
          </thead>
          <tbody>
            {traces.map((trace) => (
              <tr
                key={trace.traceId}
                className={selectedTrace?.traceId === trace.traceId ? "selected-row" : ""}
                onClick={() => onSelectTrace(trace)}
              >
                <td>{trace.traceId}</td>
                <td>{trace.transactionId}</td>
                <td>{trace.services}</td>
                <td>{trace.errorCodes}</td>
                <td>
                  <span className="badge badge-high">{trace.severity || "High"}</span>
                </td>
              </tr>
            ))}

            {traces.length === 0 && (
              <tr>
                <td colSpan="5" className="empty-cell">
                  No trace data returned from backend.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
