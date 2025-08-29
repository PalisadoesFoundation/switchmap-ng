import React from "react";
import { render, screen } from "@testing-library/react";
import { HistoricalChart } from "./HistoricalChart";
import { vi } from "vitest";

vi.mock("recharts", async () => {
  const Original: any = await vi.importActual("recharts");
  return {
    ...Original,
    ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
    LineChart: ({ children }: any) => <div>{children}</div>,
    XAxis: () => <div data-testid="x-axis" />,
    YAxis: () => <div data-testid="y-axis" />,
    Tooltip: () => <div data-testid="tooltip" />,
    Line: () => <div data-testid="line" />,
    CartesianGrid: () => <div data-testid="grid" />,
  };
});

const mockData = [
  { lastPolled: "2025-08-01", value: 1 },
  { lastPolled: "2025-08-02", value: 0 },
];

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
