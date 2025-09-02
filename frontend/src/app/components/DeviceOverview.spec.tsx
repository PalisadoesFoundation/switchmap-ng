/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DevicesOverview } from "./DevicesOverview";
import { mockDevice } from "./__mocks__/deviceMocks";

// Mock next/link to render children directly
vi.mock("next/link", () => ({ default: ({ children }: any) => children }));

describe("DevicesOverview", () => {
  it("renders loading state", () => {
    render(<DevicesOverview devices={[]} loading={true} error={null} />);
    expect(screen.getByText(/loading devices/i)).toBeInTheDocument();
  });

  it("renders error state", () => {
    render(<DevicesOverview devices={[]} loading={false} error="Failed" />);
    expect(screen.getByText(/error loading devices/i)).toBeInTheDocument();
  });

  it("renders no devices found message", () => {
    render(<DevicesOverview devices={[]} loading={false} error={null} />);
    expect(screen.getByText(/no devices found/i)).toBeInTheDocument();
  });

  it("renders table with devices", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );
    expect(screen.getByText(/devices overview/i)).toBeInTheDocument();
    expect(screen.getByText(/device 1/i)).toBeInTheDocument();
    expect(screen.getByText(/host1/i)).toBeInTheDocument();
    expect(screen.getByText(/1\/1/i)).toBeInTheDocument(); // active/total ports
  });

  it("updates global filter input", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );
    const input = screen.getByPlaceholderText(/search/i);
    fireEvent.change(input, { target: { value: "Device 1" } });
    expect((input as HTMLInputElement).value).toBe("Device 1");
  });
});
