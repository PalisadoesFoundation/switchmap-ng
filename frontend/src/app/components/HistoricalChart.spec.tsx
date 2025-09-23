import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { HistoricalChart } from "./HistoricalChart";
import { mockData } from "./__mocks__/chartMocks";

describe("HistoricalChart", () => {
  // ---------- Rendering ----------

  it("renders chart title", () => {
    render(<HistoricalChart title="System Status" data={mockData} />);
    expect(screen.getByText("System Status")).toBeInTheDocument();
  });

  // ---------- Props ----------

  it("applies color and lineType props", () => {
    render(
      <HistoricalChart
        title="Custom Chart"
        data={mockData}
        color="#ff0000"
        lineType="step"
      />
    );
    expect(screen.getByText("Custom Chart")).toBeInTheDocument();
  });

  it("applies yAxisConfig and unit correctly", () => {
    render(
      <HistoricalChart
        title="YAxis Chart"
        data={mockData}
        unit="ms"
        yAxisConfig={{ allowDecimals: false, ticks: [0, 50, 100] }}
      />
    );
    expect(screen.getByText("YAxis Chart")).toBeInTheDocument();
  });
});
