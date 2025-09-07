/// <reference types="vitest" />
import React from "react";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from "@testing-library/react";
import { describe, it, vi, expect, beforeEach, afterEach } from "vitest";
import Home from "./page";

// --- Mock child components ---
vi.mock("./components/Sidebar", () => ({
  Sidebar: () => <div data-testid="sidebar">Sidebar</div>,
}));

vi.mock("./components/ZoneDropdown", () => ({
  ZoneDropdown: ({ selectedZoneId, onChange }: any) => (
    <select
      data-testid="zone-dropdown"
      value={selectedZoneId}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="">Select zone</option>
      <option value="1">Zone 1</option>
      <option value="2">Zone 2</option>
    </select>
  ),
}));
vi.mock("./components/TopologyChart", () => ({
  TopologyChart: ({ devices, error }: any) => (
    <div data-testid="topology-chart">
      {error ? `Error: ${error}` : `TopologyChart: ${devices.length} devices`}
    </div>
  ),
}));

vi.mock("./components/DevicesOverview", () => ({
  DevicesOverview: ({ devices, error }: any) => (
    <div data-testid="devices-overview">
      {error ? `Error: ${error}` : `DevicesOverview: ${devices.length} devices`}
    </div>
  ),
}));

// --- Mock localStorage ---
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => (store[key] = value)),
    removeItem: vi.fn((key: string) => delete store[key]),
    clear: vi.fn(() => (store = {})),
    key: vi.fn((index: number) => Object.keys(store)[index] || null),
    length: 0,
  };
})() as unknown as Storage;

describe("Home page", () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
    vi.spyOn(window, "localStorage", "get").mockReturnValue(localStorageMock);
    localStorageMock.clear();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it("renders sidebar and zone dropdown", () => {
    render(<Home />);
    expect(screen.getByTestId("sidebar")).toBeInTheDocument();
    expect(screen.getByTestId("zone-dropdown")).toBeInTheDocument();
  });

  it("fetches devices when zone is selected", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: {
          zone: {
            devices: {
              edges: [
                {
                  node: { idxDevice: 1, hostname: "Device1", sysName: "Sys1" },
                },
              ],
            },
          },
        },
      }),
    });

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");
    fireEvent.change(dropdown, { target: { value: "1" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "TopologyChart: 1 devices"
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "DevicesOverview: 1 devices"
    );
    expect(localStorageMock.setItem).toHaveBeenCalledWith("zoneId", "1");
  });

  it("scrolls to element if hash exists", () => {
    // Set a hash in the URL
    window.location.hash = "#devices-overview";

    // Create a matching element in the DOM
    const element = document.createElement("div");
    element.id = "devices-overview";
    document.body.appendChild(element);

    // Mock scrollIntoView
    element.scrollIntoView = vi.fn();

    render(<Home />);

    expect(element.scrollIntoView).toHaveBeenCalledWith({ behavior: "smooth" });

    // Clean up
    document.body.removeChild(element);
    window.location.hash = "";
  });
  it(
    "handles unknown errors correctly",
    async () => {
      // Throw a non-Error to hit the 'unknown error' branch
      (global.fetch as any).mockImplementation(() => {
        throw "fail string";
      });

      render(<Home />);
      const dropdown = screen.getByTestId("zone-dropdown");
      fireEvent.change(dropdown, { target: { value: "1" } });

      // Wait long enough for retries: first retry 1s, second retry 2s
      await waitFor(
        () =>
          expect(screen.getByTestId("topology-chart")).toHaveTextContent(
            "Error: Failed to load devices. Please check your network or try again."
          ),
        { timeout: 7000 } // give it enough time for 2 retries
      );

      expect(screen.getByTestId("devices-overview")).toHaveTextContent(
        "Error: Failed to load devices. Please check your network or try again."
      );
    },
    { timeout: 7000 }
  );
});
