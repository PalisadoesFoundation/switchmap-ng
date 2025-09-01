// TopologyChart.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import React from "react";
import { TopologyChart } from "./TopologyChart";
import { mockDevice } from "./__mocks__/deviceMocks";

// Inline mock for vis-network
vi.mock("vis-network/standalone/esm/vis-network", () => ({
  Network: vi.fn().mockImplementation(() => ({
    fit: vi.fn(),
    moveTo: vi.fn(),
    on: vi.fn(),
    unselectAll: vi.fn(),
  })),
  DataSet: vi.fn().mockImplementation((data) => ({
    get: vi.fn(() => data),
    add: vi.fn(),
    clear: vi.fn(),
    update: vi.fn(),
  })),
}));

describe("TopologyChart", () => {
  it("renders loading state", () => {
    render(<TopologyChart devices={[]} loading={true} error={null} />);
    expect(screen.getByText(/loading topology/i)).toBeInTheDocument();
  });

  it("renders error state", () => {
    render(<TopologyChart devices={[]} loading={false} error="Failed" />);
    expect(screen.getByText(/error loading topology/i)).toBeInTheDocument();
  });

  it("renders graph with devices", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/search device/i)).toBeInTheDocument();
  });

  it("updates search suggestions", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const input = screen.getByPlaceholderText(/search device/i);
    fireEvent.change(input, { target: { value: "Device" } });
    expect(screen.getByText("Device 1")).toBeInTheDocument();
  });

  it("resets graph on reset button click", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const resetBtn = screen.getByText(/reset/i);
    fireEvent.click(resetBtn);
    expect(screen.getByText(/network topology/i)).toBeInTheDocument();
  });
});
