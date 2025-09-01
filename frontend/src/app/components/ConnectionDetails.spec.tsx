/// <reference types="vitest" />
import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ConnectionDetails } from "./ConnectionDetails";
import { mockDevice } from "./__mocks__/deviceMocks";

// Mock next/navigation globally in vitest.setup.ts
vi.mock("next/navigation", () => ({ useParams: () => ({ deviceId: "1" }) }));

describe("ConnectionDetails", () => {
  it("renders no data message when device is null", () => {
    render(<ConnectionDetails device={null as any} />);
    expect(
      screen.getByText(/no interface data available/i)
    ).toBeInTheDocument();
  });

  it("renders table with device interfaces", () => {
    render(<ConnectionDetails device={mockDevice} />);
    expect(screen.getByText(/connection details/i)).toBeInTheDocument();
    expect(screen.getByText("Port")).toBeInTheDocument();
    expect(screen.getByText("VLAN")).toBeInTheDocument();
    expect(screen.getByText("Mac Address")).toBeInTheDocument();
  });

  it("extracts MAC addresses correctly", () => {
    render(<ConnectionDetails device={mockDevice} />);
    const macCell = screen.getByText((content) =>
      content.includes("00:11:22:33:44:55")
    );
    expect(macCell).toBeInTheDocument();
  });

  it("extracts manufacturers correctly", () => {
    render(<ConnectionDetails device={mockDevice} />);
    const manuCell = screen.getByText((content) => content.includes("Cisco"));
    expect(manuCell).toBeInTheDocument();
  });
});
