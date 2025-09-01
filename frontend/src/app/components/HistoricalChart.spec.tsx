import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { HistoricalChart } from "./HistoricalChart";
import { mockData } from "./__mocks__/chartMocks";

vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
  LineChart: ({ children }: any) => <div>{children}</div>,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Line: () => <div data-testid="line" />,
  CartesianGrid: () => <div data-testid="grid" />,
}));
describe("HistoricalChart", () => {
  it("renders chart title", () => {
    render(<HistoricalChart title="System Status" data={mockData} />);
    expect(screen.getByText("System Status")).toBeInTheDocument();
  });

  it("renders Y-axis", () => {
    render(<HistoricalChart title="System Status" data={mockData} />);
    expect(screen.getByTestId("y-axis")).toBeInTheDocument();
  });

  it("renders X-axis", () => {
    render(<HistoricalChart title="System Status" data={mockData} />);
    expect(screen.getByTestId("x-axis")).toBeInTheDocument();
  });

  it("renders Line component", () => {
    render(<HistoricalChart title="System Status" data={mockData} />);
    expect(screen.getByTestId("line")).toBeInTheDocument();
  });
});
