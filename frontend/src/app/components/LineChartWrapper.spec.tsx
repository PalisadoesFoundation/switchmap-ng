import { render } from "@testing-library/react";
import { LineChartWrapper } from "./LineChartWrapper";
import { vi } from "vitest";

describe("LineChartWrapper", () => {
  const mockData = [
    { time: "2025-08-01T00:00:00Z", value: 10 },
    { time: "2025-08-02T00:00:00Z", value: 20 },
  ];

  it("renders with lines and title", () => {
    const { getByText } = render(
      <LineChartWrapper
        data={mockData}
        xAxisKey="time"
        lines={[{ dataKey: "value", stroke: "#8884d8" }]}
        title="My Chart"
      />
    );

    expect(getByText("My Chart")).toBeInTheDocument();
  });

  it("accepts a tooltipFormatter", () => {
    const tooltipFormatter = vi.fn(
      (val: unknown, name: string, props: any): [React.ReactNode, string] => {
        return [`${val} units`, name];
      }
    );

    render(
      <LineChartWrapper
        data={mockData}
        xAxisKey="time"
        lines={[{ dataKey: "value", stroke: "#82ca9d" }]}
        tooltipFormatter={tooltipFormatter}
      />
    );
    expect(tooltipFormatter("10", "value", { payload: { value: 10 } })).toEqual(
      ["10 units", "value"]
    );
  });
});
