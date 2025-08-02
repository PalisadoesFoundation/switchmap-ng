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

function HistoricalChart({
  data,
  title,
  color = "#8884d8",
  unit = "",
}: HistoricalChartProps) {
  return (
    <div className="w-full h-64">
      <h2 className="mb-2 text-lg font-semibold">{title}</h2>
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
}

export default HistoricalChart;
