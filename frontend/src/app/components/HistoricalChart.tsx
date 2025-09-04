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

/**
 * HistoricalChart component renders a line chart using the Recharts library.
 * It displays historical data points with customizable options for appearance and behavior.
 * @remarks
 * This component is designed for client-side use only because it relies on
 * the Recharts library, which requires access to the DOM.
 * @param data - An array of data points to be plotted on the chart.
 * @param title - The title of the chart.
 * @param color - The color of the line in the chart. Default is "#8884d8".
 * @param unit - The unit to display in the tooltip. Default is an empty string.
 * @param yAxisConfig - Configuration options for the Y-axis, including domain, ticks, tickFormatter, and allowDecimals.
 * @param lineType - The type of line to be drawn. Options include "linear", "monotone", "step", "stepAfter", and "stepBefore". Default is "monotone".
 * @returns The rendered HistoricalChart component.
 * @see {@link LineChart}, {@link Line}, {@link XAxis}, {@link YAxis}, {@link Tooltip}, {@link CartesianGrid}, {@link ResponsiveContainer} from Recharts for chart rendering.
 */

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
          <Line type={lineType} dataKey="value" stroke={color} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default HistoricalChart;
