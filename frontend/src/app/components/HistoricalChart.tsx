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
  lastPolled: string;
  value: number;
};

interface HistoricalChartProps {
  data: DataPoint[];
  title: string;
  color?: string;
  unit?: string;
  yAxisConfig?: {
    domain?: [number, number];
    ticks?: number[];
    tickFormatter?: (v: number) => string;
    allowDecimals?: boolean;
  };
  lineType?: "linear" | "monotone" | "step" | "stepAfter" | "stepBefore";
}

function HistoricalChart({
  data,
  title,
  color = "#8884d8",
  unit = "",
  yAxisConfig,
  lineType = "monotone",
}: HistoricalChartProps) {
  return (
    <div className="w-full h-64 m-2">
      <h2 className="m-2 text-lg font-semibold">{title}</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="lastPolled" />
          <YAxis
            domain={yAxisConfig?.domain}
            ticks={yAxisConfig?.ticks}
            tickFormatter={yAxisConfig?.tickFormatter}
            allowDecimals={yAxisConfig?.allowDecimals}
          />

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
