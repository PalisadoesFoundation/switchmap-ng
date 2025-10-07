/// <reference types="vitest" />
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import DeviceHistoryChart from "@/app/history/page";
import { toMs } from "@/app/history/page";
import { filterDevicesByTimeRange, DeviceNode } from "../utils/deviceUtils";

const nowMs = Date.now();

const devices = [
  { hostname: "dev1", lastPolledMs: nowMs - 1000 },
  { hostname: "dev2", lastPolledMs: nowMs - 100000000 },
  { hostname: "dev3", lastPolledMs: undefined },
];

// Mock fetch
beforeEach(() => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      data: {
        zones: {
          edges: [
            {
              node: {
                idxZone: 1,
                name: "Zone A",
                devices: {
                  edges: [
                    {
                      node: {
                        idxDevice: 101,
                        hostname: "device1",
                        sysName: "sys-1",
                        lastPolled: Math.floor(Date.now() / 1000),
                      },
                    },
                  ],
                },
              },
            },
          ],
        },
      },
    }),
  }) as any;
});

afterEach(() => {
  vi.resetAllMocks();
});

describe("DeviceHistoryChart", () => {
  it("renders header and description", () => {
    render(<DeviceHistoryChart />);
    expect(
      screen.getByRole("heading", { name: /device history/i })
    ).toBeInTheDocument();
    expect(
      screen.getByText(/visualizing the historical movement/i)
    ).toBeInTheDocument();
  });

  it("shows loading state", async () => {
    (global.fetch as any).mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                ok: true,
                json: async () => ({ data: { zones: { edges: [] } } }),
              }),
            100
          )
        )
    );

    render(<DeviceHistoryChart />);
    expect(await screen.findByText(/loading devices/i)).toBeInTheDocument();
  });

  it("shows results after fetch", async () => {
    (global.fetch as any) = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => [{ hostname: "device1", status: "active" }],
    });

    render(<DeviceHistoryChart />);
    const input = screen.getByPlaceholderText("Search device hostname...");
    const button = screen.getByRole("button", { name: /search/i });
    fireEvent.change(input, { target: { value: "device1" } });
    fireEvent.click(button);

    const result = await screen.findByText(
      (_, element) =>
        element?.tagName === "P" &&
        element.textContent?.includes("Showing results for Hostname: device1")
    );

    expect(result).toBeInTheDocument();
  });

  it("allows changing date range", async () => {
    render(<DeviceHistoryChart />);

    const button = await screen.findByRole("button", { name: /past 1 week/i });
    fireEvent.click(button);

    fireEvent.click(await screen.findByText(/past 1 day/i));
    expect(
      await screen.findByRole("button", { name: /past 1 day/i })
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /past 1 day/i }));
    fireEvent.click(await screen.findByText(/past 1 month/i));
    expect(
      await screen.findByRole("button", { name: /past 1 month/i })
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /past 1 month/i }));
    fireEvent.click(await screen.findByText(/past 6 months/i));
    expect(
      await screen.findByRole("button", { name: /past 6 months/i })
    ).toBeInTheDocument();
  });

  it("shows an error when custom range exceeds 180 days", async () => {
    render(<DeviceHistoryChart />);
    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");
    fireEvent.change(endInput, { target: { value: "2025-08-01" } });
    fireEvent.change(startInput, { target: { value: "2025-01-01" } });

    expect(
      await screen.findByText(/custom range cannot exceed 180 days/i)
    ).toBeInTheDocument();
  });

  it("accepts a valid custom date range without showing an error", async () => {
    render(<DeviceHistoryChart />);

    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    fireEvent.change(startInput, { target: { value: "2025-01-01" } });
    fireEvent.change(endInput, { target: { value: "2025-01-15" } });

    expect(
      screen.queryByText(/custom range cannot exceed 180 days/i)
    ).not.toBeInTheDocument();
  });
  it("shows 'No results found.' when fetch fails", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("boom"));
    render(<DeviceHistoryChart />);
    expect(await screen.findByText(/no results found/i)).toBeInTheDocument();
  });

  it("does not search when input is empty", async () => {
    render(<DeviceHistoryChart />);

    const form = screen.getByRole("form");
    const input = screen.getByPlaceholderText(/search device hostname/i);
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.submit(form);
    expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument();
  });
  it("submits search term when input is non-empty", async () => {
    render(<DeviceHistoryChart />);

    const form = screen.getByRole("form");
    const input = screen.getByPlaceholderText(/search device hostname/i);

    fireEvent.change(input, { target: { value: "device1" } });
    fireEvent.submit(form);
    expect(input).toHaveValue("");
    expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument();
  });

  it("renders no results message when fetch fails", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("boom"));

    render(<DeviceHistoryChart />);
    expect(await screen.findByText(/no results found/i)).toBeInTheDocument();
  });

  it("shows an error when end date is before start date", async () => {
    render(<DeviceHistoryChart />);
    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");
    fireEvent.change(startInput, { target: { value: "2025-08-01" } });
    fireEvent.change(endInput, { target: { value: "2025-01-01" } });

    expect(
      await screen.findByText(/end date must be after start date/i)
    ).toBeInTheDocument();
  });

  it("shows an error when custom range exceeds 180 days", async () => {
    render(<DeviceHistoryChart />);

    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    fireEvent.change(startInput, { target: { value: "2025-01-01" } });
    fireEvent.change(endInput, { target: { value: "2025-08-01" } }); // >180 days

    expect(
      await screen.findByText(/custom range cannot exceed 180 days/i)
    ).toBeInTheDocument();
  });
  it("shows an error when start date is after end date", async () => {
    render(<DeviceHistoryChart />);
    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");
    fireEvent.change(endInput, { target: { value: "2025-01-01" } });
    fireEvent.change(startInput, { target: { value: "2025-08-01" } });

    expect(
      await screen.findByText(/start date must be before end date/i)
    ).toBeInTheDocument();
  });
  it("correctly converts different values to milliseconds", () => {
    expect(toMs(null)).toBeNull();
    expect(toMs(undefined)).toBeNull();
    expect(toMs(12345)).toBe(12345 * 1000);
    expect(toMs(1e12)).toBe(1e12);
    const dateStr = "2025-10-08T00:00:00Z";
    expect(toMs(dateStr)).toBe(Date.parse(dateStr));
    expect(toMs("invalid-date")).toBeNull();
  });
});

describe("filterDevicesByTimeRange", () => {
  it("filters devices for custom range", () => {
    const today = new Date();
    const start = `${today.getFullYear()}-${String(
      today.getMonth() + 1
    ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
    const end = start;

    const devices = [
      { hostname: "dev1", lastPolledMs: Date.now() },
      { hostname: "dev2", lastPolledMs: Date.now() - 100000000 },
      { hostname: "dev3", lastPolledMs: undefined },
    ];

    const result = filterDevicesByTimeRange(devices, "custom", start, end);
    expect(result.map((d) => d.hostname)).toContain("dev1");
    expect(result.map((d) => d.hostname)).not.toContain("dev2");
    expect(result.map((d) => d.hostname)).not.toContain("dev3");
  });

  it("filters devices for 1d range", () => {
    const result = filterDevicesByTimeRange(devices, "1d");
    expect(result.map((d) => d.hostname)).toContain("dev1");
  });

  it("filters devices for 1w range", () => {
    const result = filterDevicesByTimeRange(devices, "1w");
    expect(result.map((d) => d.hostname)).toContain("dev1");
  });

  it("filters devices for 1m range", () => {
    const result = filterDevicesByTimeRange(devices, "1m");
    expect(result.map((d) => d.hostname)).toContain("dev1");
  });

  it("filters devices for 6m range", () => {
    const result = filterDevicesByTimeRange(devices, "6m");
    expect(result.map((d) => d.hostname)).toContain("dev1");
  });

  it("returns unfiltered devices if timeRange is invalid", () => {
    const result = filterDevicesByTimeRange(devices, "invalid");
    expect(result.length).toBe(devices.length);
  });
});
