import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import Card from "./Card";

export default function ChartsSection({ overview }) {
  const errorCodes = overview.errorCodes || [];
  const errorsByService = overview.errorsByService || [];
  const errorTrend = overview.errorTrend || [];

  return (
    <div className="chart-grid">
      <Card title="Error codes" subtitle="Top failure signals from raw logs">
        <div className="chart-box">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={errorCodes}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="errorCode" tick={{ fontSize: 11 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card title="Errors by service" subtitle="Services producing error signals">
        <div className="chart-box">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={errorsByService}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="service" tick={{ fontSize: 11 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="errors" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card title="Error trend" subtitle="Errors over time">
        <div className="chart-box">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={errorTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" tick={{ fontSize: 11 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Line type="monotone" dataKey="errors" strokeWidth={3} dot />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}
