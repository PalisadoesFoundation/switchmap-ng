import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { LineChartWrapper } from "./LineChartWrapper";
import { mockLineData } from "./__mocks__/chartMocks";

describe("LineChartWrapper", () => {
  // ---------- Rendering ----------
  it("renders chart title", () => {
    render(
      <LineChartWrapper
        data={mockLineData}
        xAxisKey="time"
        lines={[{ dataKey: "value", stroke: "#8884d8" }]}
        title="My Chart"
      />
    );

    expect(screen.getByText("My Chart")).toBeInTheDocument();
  });

  // ---------- Props ----------
  it("accepts tooltipFormatter prop", () => {
    const tooltipFormatter = vi.fn(
      (val: unknown, name: string, props: any): [React.ReactNode, string] => {
        return [`${val} units`, name];
      }
    );

    render(
      <LineChartWrapper
        data={mockLineData}
        xAxisKey="time"
        lines={[{ dataKey: "value", stroke: "#82ca9d" }]}
        tooltipFormatter={tooltipFormatter}
      />
    );
    expect(tooltipFormatter("10", "value", { payload: { value: 10 } })).toEqual(
      ["10 units", "value"]
    );
  });

  // ---------- Functions / Inline logic ----------
  it("executes tickFormatter with locale-aware expectations", () => {
    const tickFormatter = (t: string) =>
      new Date(t).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
      });

    const expected0 = new Date(mockLineData[0].time).toLocaleDateString(
      undefined,
      { month: "short", day: "numeric" }
    );
    const expected1 = new Date(mockLineData[1].time).toLocaleDateString(
      undefined,
      { month: "short", day: "numeric" }
    );
    expect(tickFormatter(mockLineData[0].time)).toBe(expected0);
    expect(tickFormatter(mockLineData[1].time)).toBe(expected1);
  });
});
