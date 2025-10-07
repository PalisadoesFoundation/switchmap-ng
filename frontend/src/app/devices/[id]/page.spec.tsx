/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";

// Import the component
import DevicePage from "./page";

// ---- Mock next/navigation ----
vi.mock("next/navigation", () => ({
  useParams: () => ({ id: "123" }),
  useSearchParams: () => new URLSearchParams(),
  useRouter: () => ({ replace: vi.fn(), push: vi.fn() }),
}));

// ---- Mock ThemeToggle ----
vi.mock("@/app/theme-toggle", () => ({
  ThemeToggle: () => <div data-testid="theme-toggle">ThemeToggle</div>,
}));

// ---- Mock DeviceDetails and ConnectionDetails ----
vi.mock("@/app/components/DeviceDetails", () => ({
  DeviceDetails: ({ device }: any) => (
    <div data-testid="device-details">{device.sysName}</div>
  ),
}));
vi.mock("@/app/components/ConnectionDetails", () => ({
  ConnectionDetails: ({ device }: any) => (
    <div data-testid="connection-details">{device.hostname}</div>
  ),
}));

// ---- Helpers ----
const mockDevice = {
  id: "1",
  idxDevice: 1,
  sysName: "TestDevice",
  hostname: "testhost",
};

describe("DevicePage", () => {
  beforeEach(() => {
    // Mock matchMedia
    vi.stubGlobal("matchMedia", (query: string) => {
      return {
        matches: true,
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        onchange: null,
        dispatchEvent: vi.fn(),
      };
    });

    // Mock fetch
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              data: { device: mockDevice },
            }),
        })
      ) as any
    );
  });

  it("renders with sidebar expanded", async () => {
    render(<DevicePage />);
    await waitFor(() => {
      expect(screen.getByTestId("device-details")).toHaveTextContent(
        "TestDevice"
      );
    });

    expect(screen.getByTestId("theme-toggle")).toBeInTheDocument();
    expect(screen.getByText("Device Overview")).toBeInTheDocument();
    expect(screen.getByText("Connection Details")).toBeInTheDocument();
  });

  it("switches tabs when clicked", async () => {
    render(<DevicePage />);
    await waitFor(() => screen.getByTestId("device-details"));

    fireEvent.click(screen.getByText("Connection Details"));

    await waitFor(() => {
      expect(screen.getByTestId("connection-details")).toHaveTextContent(
        "testhost"
      );
    });
  });

  it("collapses and expands sidebar", async () => {
    render(<DevicePage />);
    await waitFor(() => screen.getByTestId("device-details"));

    const toggleButton = screen.getByLabelText("Collapse sidebar");
    fireEvent.click(toggleButton);

    expect(screen.getByLabelText("Expand sidebar")).toBeInTheDocument();
  });

  it("handles fetch error gracefully", async () => {
    // Mock fetch to fail
    (fetch as any).mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        json: async () => ({ errors: [{ message: "Server error" }] }),
      })
    );

    render(<DevicePage />);
    const deviceEl = await screen.findByTestId("device-details");
    expect(deviceEl).toHaveTextContent(/Unnamed Device|TestDevice/i);
  });
});
