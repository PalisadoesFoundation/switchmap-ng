/// <reference types="vitest" />
import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
} from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import DeviceHistoryChart, {
  toMs,
  filterDevicesByTimeRange,
} from "@/app/history/page";

import { deviceCache } from "@/app/history/page";

type MockDeviceNode = {
  idxDevice: number;
  hostname: string;
  sysName: string;
  zone?: string;
  lastPolled?: number | null;
  lastPolledMs?: number | null;
};

const nowSec = Math.floor(Date.now() / 1000);

const mockDeviceResponse = {
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
                    lastPolled: nowSec,
                  },
                },
                {
                  node: {
                    idxDevice: 2,
                    hostname: "host1",
                    sysName: "Device 1-Updated",
                    lastPolled: nowSec - 3600,
                  },
                },
                {
                  node: {
                    idxDevice: 3,
                    hostname: "host2",
                    sysName: "Device 2",
                    lastPolled: nowSec - 86400,
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
                    idxDevice: 4,
                    hostname: "host1",
                    sysName: "Device 1-Zone-B",
                    lastPolled: nowSec - 7200,
                  },
                },
                {
                  node: {
                    idxDevice: 5,
                    hostname: "host2",
                    sysName: "Device 2",
                    lastPolled: nowSec - 172800,
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
  vi.restoreAllMocks();
  vi.resetModules();
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => mockDeviceResponse,
  }) as any;
  deviceCache.clear();
});

afterEach(() => {
  vi.resetAllMocks();
  cleanup();
});

function byTextContent(text: string) {
  return (_: string, node: Element | null): boolean =>
    !!node && !!node.textContent?.toLowerCase().includes(text.toLowerCase());
}

describe("DeviceHistoryChart", () => {
  it("renders header, description, and search", () => {
    render(<DeviceHistoryChart />);
    expect(
      screen.getByRole("heading", { name: /device history/i })
    ).toBeInTheDocument();
    const description = screen.getAllByText(
      byTextContent("visualizing the historical movement")
    )[0];
    expect(description).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Search device hostname...")
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /search/i })).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /past 1 week/i })
    ).toBeInTheDocument();
  });

  it("shows loading, then results, then charts on search", async () => {
    let resolvePromise: any;
    const promise = new Promise((resolve) => {
      resolvePromise = resolve;
    });
    (global.fetch as any).mockImplementationOnce(() => promise);
    render(<DeviceHistoryChart />);
    await waitFor(() => {
      const loadingElements = screen.queryAllByText(
        byTextContent("loading devices")
      );
      expect(loadingElements.length).toBe(0);
    });

    resolvePromise({ ok: true, json: async () => mockDeviceResponse });
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );

    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host1" } });
    fireEvent.submit(screen.getByRole("form"));
    await waitFor(() =>
      expect(screen.getByText("Zone History")).toBeInTheDocument()
    );
  });

  it("shows no results for fetch fail", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("err"));
    render(<DeviceHistoryChart />);
    await screen.findByText(/no results found/i);
  });

  it("shows no results for HTTP fail", async () => {
    (global.fetch as any).mockResolvedValueOnce({ ok: false, status: 500 });
    render(<DeviceHistoryChart />);
    await screen.findByText(/no results found/i);
  });

  it("shows no results for GraphQL error", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ errors: [{ message: "fail" }] }),
    });
    render(<DeviceHistoryChart />);
    await screen.findByText(/no results found/i);
  });

  it("shows no results for empty data", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: { zones: { edges: [] } } }),
    });
    render(<DeviceHistoryChart />);
    await screen.findByText(/no results found/i);
  });

  it("shows and selects suggestions, clears suggestions", async () => {
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host" } });
    await waitFor(() =>
      expect(screen.getByTestId("suggestions-list")).toBeInTheDocument()
    );
    fireEvent.change(input, { target: { value: "" } });
    await waitFor(() =>
      expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument()
    );

    fireEvent.change(input, { target: { value: "host" } });
    await waitFor(() =>
      expect(screen.getByTestId("suggestions-list")).toBeInTheDocument()
    );
    const firstSuggestion = screen
      .getByTestId("suggestions-list")
      .querySelector("li");
    if (firstSuggestion) {
      fireEvent.click(firstSuggestion);
      await waitFor(() => {
        const matches = screen.getAllByText(
          byTextContent("showing results for hostname")
        );
        expect(matches[0]).toBeInTheDocument();
      });
    }
  });

  it("does not submit search if input empty", async () => {
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
    const input = screen.getByPlaceholderText(/search device hostname/i);
    const form = screen.getByRole("form");
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.submit(form);
    expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument();
  });

  it("handles date range changes, toggles menu, and custom date errors", async () => {
    render(<DeviceHistoryChart />);

    let rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/past 1 day/i));
    expect(
      screen.getByRole("button", { name: /past 1 day/i })
    ).toBeInTheDocument();

    // Open custom date range
    fireEvent.click(screen.getByRole("button", { name: /past 1 day/i }));
    fireEvent.click(screen.getByText(/custom/i));
    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");
    expect(startInput).toBeInTheDocument();
    expect(endInput).toBeInTheDocument();

    // Invalid end date
    fireEvent.change(startInput, { target: { value: "2025-08-01" } });
    fireEvent.change(endInput, { target: { value: "2025-01-01" } });
    fireEvent.blur(endInput);
    await screen.findByText(/end date must be after start date/i);

    // Range exceeding 180 days
    fireEvent.change(startInput, { target: { value: "2025-01-01" } });
    fireEvent.change(endInput, { target: { value: "2025-08-01" } });
    fireEvent.blur(endInput);
    await screen.findByText(/custom range cannot exceed 180 days/i);

    // Switch back to predefined range
    fireEvent.click(screen.getByRole("button", { name: /custom range/i }));
    fireEvent.click(screen.getByText(/past 1 month/i));
    expect(
      screen.getByRole("button", { name: /past 1 month/i })
    ).toBeInTheDocument();
  });

  it("renders charts for search and not when there is no history", async () => {
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host1" } });
    fireEvent.submit(screen.getByRole("form"));
    await waitFor(() =>
      expect(screen.getByText("Zone History")).toBeInTheDocument()
    );
    expect(screen.getByText("SysName History")).toBeInTheDocument();

    const singleDeviceResponse = {
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
                        idxDevice: 11,
                        hostname: "single",
                        sysName: "Device 1",
                        lastPolled: nowSec,
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
      json: async () => singleDeviceResponse,
    });
    cleanup();
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
    fireEvent.change(screen.getByPlaceholderText("Search device hostname..."), {
      target: { value: "nonexistent" },
    });
    fireEvent.submit(screen.getByRole("form"));

    await waitFor(() =>
      expect(
        screen.getAllByText(byTextContent("showing results for hostname"))[0]
      ).toBeInTheDocument()
    );

    expect(screen.queryByText("Zone History")).not.toBeInTheDocument();
    expect(screen.queryByText("SysName History")).not.toBeInTheDocument();
  });

  it("handles missing fields correctly", async () => {
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
                        lastPolled: nowSec,
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
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );

    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host2" } });
    fireEvent.submit(screen.getByRole("form"));

    await waitFor(() =>
      expect(
        screen.getAllByText(byTextContent("showing results for hostname"))[0]
      ).toBeInTheDocument()
    );
  });

  it("renders multiple devices correctly", async () => {
    const manyDevicesResponse = {
      data: {
        zones: {
          edges: [
            {
              node: {
                idxZone: 1,
                name: "Zone A",
                devices: {
                  edges: Array.from({ length: 10 }, (_, i) => ({
                    node: {
                      idxDevice: i,
                      hostname: `host${i}`,
                      sysName: `Device ${i}`,
                      lastPolled: nowSec,
                    },
                  })),
                },
              },
            },
          ],
        },
      },
    };
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => manyDevicesResponse,
    });

    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
  });

  it("caches data and avoids refetching", async () => {
    vi.resetModules();

    const fetchSpy = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockDeviceResponse,
    });
    global.fetch = fetchSpy as any;
    const { default: DeviceHistoryChart } = await import("@/app/history/page");
    const { unmount } = render(<DeviceHistoryChart />);
    await waitFor(() => expect(fetchSpy).toHaveBeenCalledTimes(1));
    unmount();
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it("handles changing search term repeatedly and AbortError", async () => {
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
    const input = screen.getByPlaceholderText("Search device hostname...");
    fireEvent.change(input, { target: { value: "host1" } });
    fireEvent.submit(screen.getByRole("form"));
    await waitFor(() => expect(screen.getByText("host1")).toBeInTheDocument());
    fireEvent.change(input, { target: { value: "host2" } });
    fireEvent.submit(screen.getByRole("form"));
    await waitFor(() => expect(screen.getByText("host2")).toBeInTheDocument());

    // AbortError
    const abortError = new Error("The operation was aborted");
    abortError.name = "AbortError";
    (global.fetch as any).mockRejectedValueOnce(abortError);
    cleanup();
    render(<DeviceHistoryChart />);
    await waitFor(() =>
      expect(
        screen.queryByText(byTextContent("loading devices"))
      ).not.toBeInTheDocument()
    );
  });
});

describe("toMs function", () => {
  it("handles null, undefined, number, string, edge cases", () => {
    expect(toMs(null)).toBeNull();
    expect(toMs(undefined)).toBeNull();
    expect(toMs(12345)).toBe(12345 * 1000);
    expect(toMs(1e12)).toBe(1e12);
    const dateStr = "2025-10-08T00:00:00Z";
    expect(toMs(dateStr)).toBe(Date.parse(dateStr));
    expect(toMs("invalid-date")).toBeNull();
    expect(toMs(100)).toBe(100000);
    expect(toMs(1234567890123)).toBe(1234567890123);
  });
});

describe("filterDevicesByTimeRange", () => {
  const msNow = Date.now();
  const devices: MockDeviceNode[] = [
    {
      hostname: "dev1",
      lastPolledMs:
        new Date("2025-10-08T12:00:00").getTime() +
        new Date().getTimezoneOffset() * 60 * 1000,
      idxDevice: 0,
      sysName: "",
    },
    {
      hostname: "dev2",
      lastPolledMs: new Date("2025-10-07T12:00:00").getTime(),
      idxDevice: 1,
      sysName: "",
    }, // before range
    {
      hostname: "dev3",
      lastPolledMs: new Date("2025-10-09T12:00:00").getTime(),
      idxDevice: 2,
      sysName: "",
    }, // after range
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
    const now = Date.now();
    const testDevices: MockDeviceNode[] = [
      { hostname: "dev1", idxDevice: 0, lastPolledMs: now, sysName: "" }, // always in range
      {
        hostname: "dev2",
        idxDevice: 1,
        lastPolledMs: now - 10 * 24 * 60 * 60 * 1000,
        sysName: "",
      }, // outside 1d
    ];

    ["1d", "1w", "1m", "6m"].forEach((range) => {
      const result = filterDevicesByTimeRange(testDevices, range);
      expect(result).toContainEqual(testDevices[0]);
    });
  });

  it("returns all devices if custom range selected but start/end missing", () => {
    const result = filterDevicesByTimeRange(devices, "custom");
    expect(result).toEqual(devices);
  });

  it("filters devices with null lastPolledMs", () => {
    const testDevices: MockDeviceNode[] = [
      { idxDevice: 4, hostname: "devNull", sysName: "t", lastPolledMs: null },
      {
        idxDevice: 5,
        hostname: "devValid",
        sysName: "t",
        lastPolledMs: Date.now(),
      },
    ];
    const result = filterDevicesByTimeRange(testDevices, "1d");
    expect(result.map((d) => d.hostname)).toContain("devValid");
    expect(result.map((d) => d.hostname)).not.toContain("devNull");
  });

  it("handles devices outside time range", () => {
    const oldDevices: MockDeviceNode[] = [
      {
        idxDevice: 6,
        hostname: "old",
        sysName: "t",
        lastPolledMs: Date.now() - 86400000 * 8,
      },
      {
        idxDevice: 7,
        hostname: "recent",
        sysName: "t",
        lastPolledMs: Date.now() - 3600000,
      },
    ];
    const result = filterDevicesByTimeRange(oldDevices, "1d");
    expect(result.map((d) => d.hostname)).toContain("recent");
    expect(result.map((d) => d.hostname)).not.toContain("old");
  });

  it("handles empty devices and unknown range", () => {
    expect(filterDevicesByTimeRange([], "unknown")).toEqual([]);
    const many: MockDeviceNode[] = [
      { idxDevice: 8, hostname: "a", sysName: "na", lastPolledMs: undefined },
      { idxDevice: 9, hostname: "b", sysName: "nb", lastPolledMs: null },
      { idxDevice: 10, hostname: "c", sysName: "nc", lastPolledMs: NaN },
    ];
    expect(filterDevicesByTimeRange(many, "custom")).toEqual(many);
  });
});
