"use client";
import React from "react";
import type { AxisDomain } from "recharts/types/util/types";
import type {
  Payload,
  ValueType,
} from "recharts/types/component/DefaultTooltipContent";
import {
  ResponsiveContainer,
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  Line,
} from "recharts";

interface DotProps {
  cx?: number;
  cy?: number;
  payload?: unknown;
  value?: unknown;
}

interface TickProps {
  x?: number;
  y?: number;
  payload?: {
    value?: unknown;
  };
}

interface LineConfig {
  dataKey: string;
  stroke: string;
  type?: "monotone" | "linear" | "stepAfter" | "stepBefore";
  dot?:
    | boolean
    | object
    | React.ReactElement<SVGElement>
    | ((props: DotProps) => React.ReactNode);
  isAnimationActive?: boolean;
  strokeWidth?: number;
}

interface YAxisConfig {
  type?: "number" | "category";
  domain?: AxisDomain;
  ticks?: Array<number | string>;
  tickFormatter?: (value: number | string, index: number) => string;
  width?: number;
  tick?:
    | boolean
    | object
    | React.ReactElement<SVGElement>
    | ((props: TickProps) => React.ReactElement<SVGElement>);
}

interface TooltipFormatterProps {
  value?: unknown;
  name?: string;
  payload?: Record<string, unknown>;
  dataKey?: string;
  color?: string;
}

interface LineChartWrapperProps<T = Record<string, unknown>> {
  data: T[];
  xAxisKey: keyof T;
  lines: LineConfig[];
  yAxisConfig?: YAxisConfig;
  title?: string;
  height?: number;
  tooltipFormatter?: (
    value: ValueType,
    name: string,
    props: Payload<ValueType, string>
  ) => React.ReactNode | [React.ReactNode, string];
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
 * @see {@link LineChart}, {@link XAxis}, {@link YAxis}, {@link Tooltip}, {@link Line} from Recharts for chart rendering.
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
                value: ValueType,
                name: string,
                props: Payload<ValueType, string>
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
              isAnimationActive={line.isAnimationActive}
              strokeWidth={line.strokeWidth}
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
