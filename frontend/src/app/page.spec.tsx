/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, vi, expect, beforeEach, afterEach } from "vitest";
import Home, { _testUtils } from "./page";

// ----- Mock Child Components -----
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
      <option value="all">All</option>
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

// ----- Mock localStorage -----
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

// ----- Test Suite -----
describe("Home page", () => {
  let originalFetch: any;

  // ----- Setup & Teardown -----
  beforeEach(() => {
    _testUtils.clearDeviceCache();
    originalFetch = global.fetch;
    vi.spyOn(window, "localStorage", "get").mockReturnValue(localStorageMock);
    localStorageMock.clear();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  // ----- Rendering -----
  it("renders sidebar and zone dropdown", () => {
    render(<Home />);
    expect(screen.getByTestId("sidebar")).toBeInTheDocument();
    expect(screen.getByTestId("zone-dropdown")).toBeInTheDocument();
  });

  // ----- Fetch & Deduplication -----
  it("fetches and deduplicates devices when zone is selected", async () => {
    const mockZones = [
      {
        node: {
          devices: {
            edges: [
              { node: { hostname: "Device1", idxDevice: 1 } },
              { node: { hostname: "Device1", idxDevice: 2 } },
              { node: { hostname: "Device2", idxDevice: 3 } },
            ],
          },
        },
      },
    ];

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: async () => ({
          data: {
            zones: {
              edges: mockZones,
            },
          },
        }),
      } as any)
    );

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");

    fireEvent.change(dropdown, { target: { value: "all" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "TopologyChart: 2 devices"
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "DevicesOverview: 2 devices"
    );
    expect(localStorageMock.setItem).toHaveBeenCalledWith("zoneId", "all");
  });
  it("fetches and deduplicates devices for a single zone", async () => {
    // Mock fetch response for a single zone
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: async () => ({
          data: {
            zone: {
              devices: {
                edges: [
                  { node: { hostname: "DeviceA", idxDevice: 1 } },
                  { node: { hostname: "DeviceA", idxDevice: 2 } },
                  { node: { hostname: "DeviceB", idxDevice: 3 } },
                ],
              },
            },
          },
        }),
      } as any)
    );

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");

    fireEvent.change(dropdown, { target: { value: "1" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "TopologyChart: 2 devices"
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "DevicesOverview: 2 devices"
    );
    expect(localStorageMock.setItem).toHaveBeenCalledWith("zoneId", "1");
  });

  // ----- Error Handling -----
  it("handles network error correctly", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: "Server Error",
        json: async () => ({}),
      } as any)
    );

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");
    fireEvent.change(dropdown, { target: { value: "1" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "Error: Network error: Server Error"
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "Error: Network error: Server Error"
    );
  });

  it("handles GraphQL errors correctly", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: async () => ({ errors: [{ message: "GraphQL failed" }] }),
      } as any)
    );

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");
    fireEvent.change(dropdown, { target: { value: "1" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "Error: GraphQL failed"
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "Error: GraphQL failed"
    );
  });

  it("handles unknown thrown errors correctly", async () => {
    global.fetch = vi.fn(() => Promise.reject("Unknown failure"));

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");
    fireEvent.change(dropdown, { target: { value: "all" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "Error: Unknown failure"
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "Error: Unknown failure"
    );
  });
  it("handles non-error, non-string failures", async () => {
    global.fetch = vi.fn(() => Promise.reject({ some: "object" }));

    render(<Home />);
    const dropdown = screen.getByTestId("zone-dropdown");
    fireEvent.change(dropdown, { target: { value: "all" } });

    await waitFor(() =>
      expect(screen.getByTestId("topology-chart")).toHaveTextContent(
        "Error: Failed to load devices. Please check your network or try again."
      )
    );
    expect(screen.getByTestId("devices-overview")).toHaveTextContent(
      "Error: Failed to load devices. Please check your network or try again."
    );
  });

  // ----- Scroll Behavior -----
  it("scrolls to element if hash exists", async () => {
    window.location.hash = "#devices-overview";

    const element = document.createElement("div");
    element.id = "devices-overview";
    document.body.appendChild(element);

    element.scrollIntoView = vi.fn();

    render(<Home />);

    await waitFor(() => {
      expect(element.scrollIntoView).toHaveBeenCalledWith({
        behavior: "smooth",
      });
    });

    document.body.removeChild(element);
    window.location.hash = "";
  });
});
