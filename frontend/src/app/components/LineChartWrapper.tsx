import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  Line,
} from "recharts";
interface LineConfig {
  dataKey: string;
  stroke: string;
  type?: "monotone" | "linear" | "stepAfter" | "stepBefore";
  dot?: boolean | Record<string, unknown>;
}

interface YAxisConfig {
  type?: "number" | "category";
  domain?: [number, number];
  ticks?: number[];
  tickFormatter?: (value: number | string) => string;
  width?: number;
  tick?: Record<string, unknown>;
}

interface LineChartWrapperProps<T = Record<string, unknown>> {
  data: T[];
  xAxisKey: keyof T;
  lines: LineConfig[];
  yAxisConfig?: YAxisConfig;
  title?: string;
  height?: number;
  tooltipFormatter?: (
    value: unknown,
    name: string,
    props: any
  ) => [React.ReactNode, string];
}
/** * LineChartWrapper is a reusable component for rendering line charts with Recharts.
 * It abstracts the common configuration for line charts, including axes, tooltips, and lines.
 * This allows for consistent styling and behavior across different charts in the application.
 * @remarks
 * This component is designed to be flexible and reusable, allowing developers to pass in data,
 * x-axis keys, line configurations, and y-axis settings.
 * It supports custom tooltips and titles, making it suitable for various charting needs.
 *
 * @returns The rendered line chart component.
 *
 * @see {@link ResponsiveContainer} for responsive layout.
 * **/
export function LineChartWrapper({
  data,
  xAxisKey,
  lines,
  yAxisConfig = {},
  title,
  height = 300,
  tooltipFormatter,
}: LineChartWrapperProps) {
  return (
    <div className="w-full flex flex-col" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ right: 20 }}>
          <XAxis
            dataKey={xAxisKey}
            tickFormatter={(t) =>
              new Date(t).toLocaleDateString(undefined, {
                month: "short",
                day: "numeric",
              })
            }
          />
          <YAxis {...yAxisConfig} />
          <Tooltip
            labelFormatter={(label) => new Date(label).toLocaleString()}
            formatter={
              tooltipFormatter as (
                value: unknown,
                name: string,
                props: any
              ) => React.ReactNode | [React.ReactNode, string]
            }
          />
          {lines.map((line) => (
            <Line
              key={line.dataKey}
              dataKey={line.dataKey}
              stroke={line.stroke}
              type={line.type || "linear"}
              dot={line.dot ?? true}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      {title && (
        <h3 className="text-lg font-semibold mt-4 text-center">{title}</h3>
      )}
    </div>
  );
}

export default LineChartWrapper;
