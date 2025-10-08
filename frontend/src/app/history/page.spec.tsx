/// <reference types="vitest" />
import {
  render,
  screen,
  fireEvent,
  waitFor,
  within,
  cleanup,
} from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import DeviceHistoryChart from "@/app/history/page";
import { toMs } from "@/app/history/page";
import { filterDevicesByTimeRange } from "../utils/deviceUtils";
const nowMs = Date.now();

type DeviceNode = {
  idxDevice: number;
  hostname: string;
  sysName: string;
  zone?: string;
  lastPolled?: number | null;
  lastPolledMs?: number | null;
};

type ZoneEdge = {
  node: {
    idxZone: number;
    name: string;
    devices: {
      edges: { node: DeviceNode }[];
    };
  };
};

type GraphQLResponse = {
  data?: {
    zones: {
      edges: ZoneEdge[];
    };
  };
  errors?: { message: string }[];
};

const mockDeviceResponse: GraphQLResponse = {
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
                    idxDevice: 1,
                    hostname: "host1",
                    sysName: "Device 1",
                    lastPolled: Math.floor(Date.now() / 1000),
                  },
                },
                {
                  node: {
                    idxDevice: 2,
                    hostname: "host2",
                    sysName: "Device 2",
                    lastPolled: Math.floor(Date.now() / 1000) - 86400,
                  },
                },
                {
                  node: {
                    idxDevice: 4,
                    hostname: "host3",
                    sysName: "Device 4",
                    lastPolled: Math.floor(Date.now() / 1000) - 172800,
                  },
                },
              ],
            },
          },
        },
        {
          node: {
            idxZone: 2,
            name: "Zone B",
            devices: {
              edges: [
                {
                  node: {
                    idxDevice: 3,
                    hostname: "host1",
                    sysName: "Device 3",
                    lastPolled: Math.floor(Date.now() / 1000) - 3600,
                  },
                },
                {
                  node: {
                    idxDevice: 5,
                    hostname: "host2",
                    sysName: "Device 5",
                    lastPolled: Math.floor(Date.now() / 1000) - 7200,
                  },
                },
              ],
            },
          },
        },
      ],
    },
  },
};

vi.mock("@/app/components/LineChartWrapper", () => ({
  LineChartWrapper: ({ title }: { title: string }) => <div>{title}</div>,
}));

beforeEach(() => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => {
      return mockDeviceResponse;
    },
  }) as any;
});

afterEach(() => {
  vi.resetAllMocks();

  // Clear the cache between tests
  if (typeof window !== "undefined" && (window as any).deviceCache) {
    (window as any).deviceCache.clear();
  }
  cleanup();
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

  it("shows results after fetch and displays hostname", async () => {
    render(<DeviceHistoryChart />);

    await waitFor(() => {
      expect(screen.queryByText(/loading devices/i)).not.toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host1" } });
    fireEvent.submit(screen.getByRole("form"));

    await waitFor(() => {
      expect(
        screen.getByText(/showing results for hostname:/i)
      ).toBeInTheDocument();
    });

    expect(screen.getByText("host1")).toBeInTheDocument();
  });

  it("submits search term when form is submitted", async () => {
    render(<DeviceHistoryChart />);

    await waitFor(() => {
      expect(screen.queryByText(/loading devices/i)).not.toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Search device hostname...");
    const form = screen.getByRole("form");

    fireEvent.change(input, { target: { value: "host1" } });
    fireEvent.submit(form);

    await waitFor(() => {
      expect(
        screen.getByText(/showing results for hostname:/i)
      ).toBeInTheDocument();
    });

    expect(input).toHaveValue("");
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

  it("shows custom date inputs when custom range is selected", async () => {
    render(<DeviceHistoryChart />);

    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    expect(screen.getByLabelText("custom start date")).toBeInTheDocument();
    expect(screen.getByLabelText("custom end date")).toBeInTheDocument();
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

    await waitFor(
      () => {
        expect(
          screen.queryByText(/custom range cannot exceed 180 days/i)
        ).not.toBeInTheDocument();
      },
      { timeout: 3500 }
    );
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

  it("shows 'No results found.' when allDevices is empty", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: { zones: { edges: [] } } }),
    });

    render(<DeviceHistoryChart />);

    expect(await screen.findByText(/no results found/i)).toBeInTheDocument();
  });

  it("shows no results message when fetch fails", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("Network error"));

    render(<DeviceHistoryChart />);

    expect(await screen.findByText(/no results found/i)).toBeInTheDocument();
  });

  it("shows no results message when HTTP response is not ok", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    render(<DeviceHistoryChart />);

    expect(await screen.findByText(/no results found/i)).toBeInTheDocument();
  });

  it("shows no results message when GraphQL returns errors", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        errors: [{ message: "GraphQL error occurred" }],
      }),
    });

    render(<DeviceHistoryChart />);

    expect(await screen.findByText(/no results found/i)).toBeInTheDocument();
  });

  it("does not search when input is empty", async () => {
    render(<DeviceHistoryChart />);

    await waitFor(() => {
      expect(screen.queryByText(/loading devices/i)).not.toBeInTheDocument();
    });

    const form = screen.getByRole("form");
    const input = screen.getByPlaceholderText(/search device hostname/i);
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.submit(form);
    expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument();
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
  it("handles devices without required fields", async () => {
    const incompleteDevicesResponse = {
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
                        idxDevice: null,
                        hostname: null,
                        sysName: "Device 1",
                        lastPolled: null,
                      },
                    },
                    {
                      node: {
                        idxDevice: 2,
                        hostname: "host2",
                        sysName: "Device 2",
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
    };

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => incompleteDevicesResponse,
    });

    render(<DeviceHistoryChart />);

    await waitFor(() => {
      expect(screen.queryByText(/loading devices/i)).not.toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host2" } });
    fireEvent.submit(screen.getByRole("form"));

    await waitFor(() => {
      expect(
        screen.getByText(/showing results for hostname:/i)
      ).toBeInTheDocument();
    });
  });

  it("toggles dropdown menu", async () => {
    render(<DeviceHistoryChart />);

    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);

    expect(screen.getByText(/past 1 day/i)).toBeInTheDocument();

    fireEvent.click(rangeButton);

    await waitFor(() => {
      expect(screen.queryByText(/past 1 day/i)).not.toBeInTheDocument();
    });
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
  const now = Date.now();
  const devices = [
    { hostname: "dev1", lastPolledMs: now }, // valid
    { hostname: "dev2", lastPolledMs: undefined }, // invalid
    { hostname: "dev3", lastPolledMs: NaN }, // invalid
  ];

  it("filters devices for custom range with valid lastPolledMs", () => {
    const start = "2025-10-08";
    const end = "2025-10-08";
    const result = filterDevicesByTimeRange(devices, "custom", start, end);
    const hostnames = result.map((d) => d.hostname);
    expect(hostnames).toContain("dev1");
    expect(hostnames).not.toContain("dev2");
    expect(hostnames).not.toContain("dev3");
  });

  it("filters devices for 1d, 1w, 1m, 6m ranges", () => {
    ["1d", "1w", "1m", "6m"].forEach((range) => {
      const result = filterDevicesByTimeRange(devices, range);
      expect(result).toContainEqual(devices[0]);
    });
  });

  it("returns all devices if custom range selected but start/end missing", () => {
    const result = filterDevicesByTimeRange(devices, "custom");
    expect(result).toEqual(devices); // matches actual function behavior
  });

  it("filters devices with null lastPolledMs", () => {
    const testDevices = [
      { hostname: "devNull", lastPolledMs: null },
      { hostname: "devValid", lastPolledMs: Date.now() },
    ];
    const result = filterDevicesByTimeRange(testDevices, "1d");
    expect(result.map((d) => d.hostname)).toContain("devValid");
    expect(result.map((d) => d.hostname)).not.toContain("devNull");
  });
});
