/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";

// Import the component
import DevicePage from "./page";

// ---- Mock next/navigation ----
vi.mock("next/navigation", () => {
  return {
    useParams: () => ({ id: "1" }),
    useSearchParams: () =>
      new URLSearchParams("sysName=TestDevice&hostname=testhost"),
    useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  };
});

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
        matches: true, // default to desktop
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

    // Wait for data load
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

    // Click "Connection Details"
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

  it("handles fetch error", async () => {
    (fetch as any).mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        status: 500,
      })
    );

    render(<DevicePage />);
    await waitFor(() => {
      expect(screen.getByText(/Error:/i)).toBeInTheDocument();
    });
  });
});
