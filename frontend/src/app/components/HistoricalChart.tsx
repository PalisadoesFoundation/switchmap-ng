import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

type DataPoint = {
  timestamp: string;
  value: number;
};

interface HistoricalChartProps {
  data: DataPoint[];
  title: string;
  color?: string;
  unit?: string;
}

const HistoricalChart: React.FC<HistoricalChartProps> = ({
  data,
  title,
  color = "#8884d8",
  unit = "",
}) => {
  return (
    <div style={{ width: "100%", height: "300px" }}>
      <h2 style={{ marginBottom: "0.5rem" }}>{title}</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip
            formatter={(value: number) => `${value}${unit}`}
            labelStyle={{ fontWeight: "bold" }}
          />
          <Line type="monotone" dataKey="value" stroke={color} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HistoricalChart;
