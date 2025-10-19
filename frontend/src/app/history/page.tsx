"use client";
import React, {
  useState,
  useEffect,
  useMemo,
  useCallback,
  lazy,
  Suspense,
} from "react";

import { Sidebar } from "../components/Sidebar";

// Lazy load the chart component
const LineChartWrapper = lazy(() =>
  import("../components/LineChartWrapper").then((mod) => ({
    default: mod.LineChartWrapper,
  }))
);

/**
 * DeviceHistoryChart component fetches and visualizes the historical movement and status changes of devices within the network.
 * It includes search functionality, time range filtering, and displays charts for zone and sysName history.
 * It handles loading and error states, and provides a user-friendly interface for exploring device history.
 *
 * Optimizations:
 * - Lazy loading of LineChartWrapper component
 * - In-memory caching of device data with TTL
 * - Debounced search input
 * - Memoized expensive computations
 * - Request cancellation with AbortController
 *
 * @remarks
 * This component is designed for client-side use only because it relies on the `useState` and `useEffect` hooks
 * to manage state and handle side effects like data fetching. It also includes interactive elements like
 * search input and dropdowns that require client-side rendering.
 * @returns A React component that renders the device history chart interface.
 * @see {@link Sidebar} for the sidebar component.
 * @see {@link LineChartWrapper} for the chart rendering component.
 */

const QUERY = `
  query ZonesWithDevices {
    zones {
      edges {
        node {
          idxZone
          name
          devices {
            edges {
              node {
                idxDevice
                hostname
                sysName
                lastPolled
              }
            }
          }
        }
      }
    }
  }
`;

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

// Cache for device data
interface CacheEntry {
  data: DeviceNode[];
  timestamp: number;
}

export const deviceCache = new Map<string, CacheEntry>();
const CACHE_DURATION = 5 * 60 * 1000;

export function toMs(value: number | string | null | undefined): number | null {
  if (value == null) return null;
  if (typeof value === "number") {
    return value < 1e12 ? value * 1000 : value;
  }
  const ms = Date.parse(value);
  return Number.isNaN(ms) ? null : ms;
}

function parseDateOnlyLocal(yyyyMmDd: string): Date {
  const [y, m, d] = yyyyMmDd.split("-").map(Number);
  return new Date(y, (m ?? 1) - 1, d ?? 1);
}

export function filterDevicesByTimeRange(
  devices: DeviceNode[],
  timeRange: string,
  start?: string,
  end?: string
): DeviceNode[] {
  const now = new Date();

  function parseDateOnlyLocal(yyyyMmDd: string): Date {
    const [y, m, d] = yyyyMmDd.split("-").map(Number);
    return new Date(y, (m ?? 1) - 1, d ?? 1);
  }

  if (timeRange === "custom" && start && end) {
    const startDate = parseDateOnlyLocal(start);
    startDate.setHours(0, 0, 0, 0);
    const endDate = parseDateOnlyLocal(end);
    endDate.setHours(23, 59, 59, 999);

    return devices.filter((d) => {
      if (typeof d.lastPolledMs !== "number") return false;
      const t = d.lastPolledMs;
      return t >= startDate.getTime() && t <= endDate.getTime();
    });
  }

  let startDate: Date | null = null;
  switch (timeRange) {
    case "1d":
      startDate = new Date(now);
      startDate.setDate(now.getDate() - 1);
      break;
    case "1w":
      startDate = new Date(now);
      startDate.setDate(now.getDate() - 7);
      break;
    case "1m":
      startDate = new Date(now);
      startDate.setMonth(now.getMonth() - 1);
      break;
    case "6m":
      startDate = new Date(now);
      startDate.setMonth(now.getMonth() - 6);
      break;
  }

  if (startDate) {
    const startMs = startDate.getTime();
    return devices.filter((d) => {
      if (typeof d.lastPolledMs !== "number") return false;
      return d.lastPolledMs >= startMs;
    });
  }

  return devices;
}

export default function DeviceHistoryChart() {
  const [allDevices, setAllDevices] = useState<DeviceNode[]>([]);
  const [allDeviceHostnames, setAllDeviceHostnames] = useState<string[]>([]);
  const [inputTerm, setInputTerm] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [range, setRange] = useState("1w");
  const [customStart, setCustomStart] = useState("");
  const [customEnd, setCustomEnd] = useState("");
  const [open, setOpen] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [ongoingRequest, setOngoingRequest] = useState<AbortController | null>(
    null
  );

  const ranges = useMemo(
    () => [
      { label: "Past 1 day", value: "1d" },
      { label: "Past 1 week", value: "1w" },
      { label: "Past 1 month", value: "1m" },
      { label: "Past 6 months", value: "6m" },
      { label: "Custom range", value: "custom" },
    ],
    []
  );

  // Check cache validity
  const getCachedDevices = useCallback(
    (cacheKey: string): DeviceNode[] | null => {
      const cached = deviceCache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        return cached.data;
      }
      return null;
    },
    []
  );

  // Fetch devices with caching and abort control
  const fetchDevices = useCallback(async () => {
    if (range === "custom" && (!customStart || !customEnd)) return;

    // Generate cache key
    const cacheKey = `${range}-${customStart}-${customEnd}`;

    // Check cache
    const cached = getCachedDevices(cacheKey);
    if (cached) {
      setAllDevices(cached);
      if (!searchTerm && cached.length > 0) {
        setSearchTerm(cached[0].hostname);
      }
      setLoading(false);
      setError(null);
      return;
    }

    // Cancel ongoing request
    if (ongoingRequest) {
      ongoingRequest.abort();
    }

    const abortController = new AbortController();
    setOngoingRequest(abortController);

    setLoading(true);
    setError(null);
    setAllDevices([]);
    setSearchTerm("");
    try {
      const endpoint =
        process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
        "http://localhost:7000/switchmap/api/graphql";

      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: QUERY }),
        signal: abortController.signal,
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: GraphQLResponse = await res.json();

      if (json.errors?.length) throw new Error(json.errors[0].message);

      const zones = json.data?.zones?.edges || [];
      let devicesWithZones: DeviceNode[] = [];

      zones.forEach((zoneEdge) => {
        const zone = zoneEdge.node;
        const deviceEdges = zone?.devices?.edges ?? [];
        deviceEdges.forEach((deviceEdge) => {
          const device = deviceEdge.node;
          if (device?.hostname && device?.idxDevice) {
            devicesWithZones.push({
              ...device,
              zone: zone.name,
              lastPolledMs: toMs(device.lastPolled ?? null),
            });
          }
        });
      });

      // Store all hostnames (unfiltered)
      setAllDeviceHostnames(
        Array.from(new Set(devicesWithZones.map((d) => d.hostname)))
      );

      // Filter by time range
      const filteredDevices = filterDevicesByTimeRange(
        devicesWithZones,
        range,
        customStart,
        customEnd
      );

      // Cache the filtered results
      deviceCache.set(cacheKey, {
        data: filteredDevices,
        timestamp: Date.now(),
      });

      setAllDevices(filteredDevices);
      if (!searchTerm && filteredDevices.length > 0) {
        setSearchTerm(filteredDevices[0].hostname);
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.name === "AbortError") {
        return; // Request was cancelled
      }
      setError(err instanceof Error ? err.message : "Error fetching devices");
    } finally {
      setLoading(false);
      setOngoingRequest(null);
    }
  }, [
    range,
    customStart,
    customEnd,
    searchTerm,
    getCachedDevices,
    filterDevicesByTimeRange,
  ]);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchDevices();
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [fetchDevices]);

  const uniqueHostnames = useMemo(() => {
    return Array.from(new Set(allDevices.map((d) => d.hostname)));
  }, [allDevices]);

  // Debounced suggestions
  useEffect(() => {
    if (inputTerm.trim() === "") {
      setSuggestions([]);
      return;
    }

    const timeoutId = setTimeout(() => {
      const filtered = allDeviceHostnames
        .filter((host) => host.toLowerCase().includes(inputTerm.toLowerCase()))
        .slice(0, 5);
      setSuggestions(filtered);
    }, 200);

    return () => clearTimeout(timeoutId);
  }, [inputTerm, allDeviceHostnames]);

  const onSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (inputTerm.trim() === "") return;
      setSearchTerm(inputTerm);
      setInputTerm("");
      setSuggestions([]);
    },
    [inputTerm]
  );

  // Memoized history calculation
  const history = useMemo(() => {
    return allDevices
      .filter(
        (d) => d.hostname === searchTerm && typeof d.lastPolledMs === "number"
      )
      .sort((a, b) => (a.lastPolledMs ?? 0) - (b.lastPolledMs ?? 0));
  }, [allDevices, searchTerm]);

  // Memoized chart data
  const { sysNameChartData, sysNameCategories, sysNameMap } = useMemo(() => {
    const categories = Array.from(new Set(history.map((h) => h.sysName)));
    const map: Record<string, number> = {};
    categories.forEach((name, i) => {
      map[name] = i + 1;
    });
    const chartData = history.map((h) => ({
      timestamp: new Date(h.lastPolledMs ?? 0).toISOString(),
      sysNameNum: map[h.sysName],
      sysName: h.sysName,
    }));
    return {
      sysNameChartData: chartData,
      sysNameCategories: categories,
      sysNameMap: map,
    };
  }, [history]);

  const { zoneChartData, zoneCategories, zoneMap } = useMemo(() => {
    const categories = Array.from(
      new Set(history.map((h) => h.zone || ""))
    ).filter(Boolean);
    const map: Record<string, number> = {};
    categories.forEach((zone, i) => {
      map[zone] = i + 1;
    });
    const chartData = history
      .filter((h) => h.zone)
      .map((h) => ({
        timestamp: new Date(h.lastPolledMs ?? 0).toISOString(),
        zoneNum: map[h.zone || ""],
        zoneName: h.zone || "",
      }));
    return {
      zoneChartData: chartData,
      zoneCategories: categories,
      zoneMap: map,
    };
  }, [history]);

  const renderFallback = useCallback(() => {
    if (loading)
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-gray-700">Loading devices...</p>
        </div>
      );
    if (error || allDevices.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-gray-700">No results found.</p>
        </div>
      );
    }
    return null;
  }, [loading, error, allDevices.length]);

  const handleDateValidation = useCallback(
    (type: "start" | "end", value: string, otherValue: string) => {
      const date = parseDateOnlyLocal(value);
      date.setHours(
        type === "start" ? 0 : 23,
        type === "start" ? 0 : 59,
        type === "start" ? 0 : 59,
        type === "start" ? 0 : 999
      );

      const other = otherValue ? parseDateOnlyLocal(otherValue) : null;
      if (other)
        other.setHours(
          type === "start" ? 23 : 0,
          type === "start" ? 59 : 0,
          type === "start" ? 59 : 0,
          type === "start" ? 999 : 0
        );

      if (
        other &&
        ((type === "start" && date > other) || (type === "end" && date < other))
      ) {
        setErrorMsg(
          `${type === "start" ? "Start" : "End"} date must be ${
            type === "start" ? "before" : "after"
          } ${type === "start" ? "end" : "start"} date.`
        );
        setTimeout(() => setErrorMsg(""), 3000);
        return false;
      }

      if (
        other &&
        Math.abs(date.getTime() - other.getTime()) / (1000 * 60 * 60 * 24) > 180
      ) {
        setErrorMsg("Custom range cannot exceed 180 days.");
        setTimeout(() => setErrorMsg(""), 3000);
        return false;
      }

      return true;
    },
    []
  );

  const LoadingFallback = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-500">Loading chart...</div>
    </div>
  );

  return (
    <div className="flex h-screen max-w-full lg:ml-60">
      {errorMsg && (
        <div className="fixed inset-0 flex mt-2 items-start justify-center z-50 pointer-events-none">
          <div className="bg-gray-300 text-gray-900 px-6 py-3 rounded shadow-lg animate-fade-in pointer-events-auto">
            {errorMsg}
          </div>
        </div>
      )}
      <div className="flex h-screen overflow-y-auto">
        <Sidebar />
        <div className="p-4 w-full max-w-full flex flex-col gap-6 h-full mr-4">
          <div className="m-4 lg:ml-0">
            <h2 className="text-xl font-semibold">Device History</h2>
            <p className="text-sm pt-2 text-gray-600">
              Visualizing the historical movement and status changes of devices
              within the network.
            </p>
          </div>

          <div className="relative flex flex-col xl:flex-row gap-10 justify-between w-full">
            <form
              className="flex flex-col gap-4 md:flex-row md:items-center"
              role="form"
              data-testid="search-form"
              onSubmit={onSubmit}
            >
              <div className="relative">
                <input
                  className="border p-2 rounded w-full"
                  type="text"
                  placeholder="Search device hostname..."
                  value={inputTerm}
                  onChange={(e) => setInputTerm(e.target.value)}
                  autoComplete="off"
                  disabled={loading}
                />
                {suggestions.length > 0 && (
                  <ul
                    className="absolute top-full left-0 mt-1 bg-bg shadow-md rounded border w-full z-50"
                    data-testid="suggestions-list"
                  >
                    {suggestions.map((suggestion, i) => (
                      <li
                        key={i}
                        onClick={() => {
                          setSearchTerm(suggestion);
                          setInputTerm("");
                          setSuggestions([]);
                        }}
                        className="cursor-pointer px-4 py-2 hover:bg-hover-bg"
                      >
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <button
                type="submit"
                className="border text-button rounded px-4 py-2 cursor-pointer transition-colors duration-300 align-middle h-fit"
                disabled={loading}
              >
                Search
              </button>
            </form>

            <div className="flex flex-row-reverse xl:flex-row gap-4 text-left justify-end xl:items-center">
              {range === "custom" && (
                <div className="flex flex-row gap-2 items-start">
                  <input
                    type="date"
                    aria-label="custom start date"
                    className="border p-2 rounded"
                    value={customStart}
                    onChange={(e) => {
                      if (
                        handleDateValidation("start", e.target.value, customEnd)
                      ) {
                        setCustomStart(e.target.value);
                      }
                    }}
                  />
                  <span className="flex items-center justify-center h-full px-2 my-auto">
                    to
                  </span>
                  <input
                    type="date"
                    aria-label="custom end date"
                    className="border p-2 rounded"
                    value={customEnd}
                    onChange={(e) => {
                      if (
                        handleDateValidation("end", e.target.value, customStart)
                      ) {
                        setCustomEnd(e.target.value);
                      }
                    }}
                  />
                </div>
              )}

              <div className="relative">
                <button
                  type="button"
                  className="flex justify-between items-center border rounded px-4 py-2 w-48"
                  onClick={() => setOpen(!open)}
                >
                  {ranges.find((r) => r.value === range)?.label}
                  <svg
                    className={`ml-2 h-5 w-5 transition-transform ${
                      open ? "rotate-180" : ""
                    }`}
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>

                {open && (
                  <div className="absolute mt-1 w-48 bg-bg border rounded shadow z-10">
                    {ranges.map((r) => (
                      <button
                        key={r.value}
                        className="w-full text-left px-4 py-2 hover:bg-hover-bg"
                        onClick={() => {
                          setRange(r.value);
                          setOpen(false);
                        }}
                      >
                        {r.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
          {searchTerm && (
            <p className="mt-2 text-gray-700">
              Showing results for Hostname:{" "}
              <span className="font-semibold">{searchTerm}</span>
            </p>
          )}

          <div className="flex-1">
            <div className="gap-8 w-[70vw] min-w-[600px] items-stretch p-4 mx-auto flex flex-col xl:flex-row xl:text-left text-center h-full">
              {renderFallback() || (
                <Suspense fallback={<LoadingFallback />}>
                  {zoneChartData.length > 0 && (
                    <LineChartWrapper
                      data-testid="device-chart"
                      data={zoneChartData}
                      xAxisKey="timestamp"
                      lines={[
                        {
                          dataKey: "zoneNum",
                          stroke: "#16a34a",
                          type: "stepAfter",
                          dot: false,
                        },
                      ]}
                      yAxisConfig={{
                        type: "number",
                        domain: [0, zoneCategories.length + 1],
                        ticks: Object.values(zoneMap),
                        tickFormatter: (v) =>
                          zoneCategories.find((z) => zoneMap[z] === v) || "",
                        width: 100,
                        tick: { textAnchor: "end" },
                      }}
                      title="Zone History"
                      tooltipFormatter={(_, __, props) => {
                        const value = props.payload.zoneNum;
                        const label =
                          zoneCategories.find((z) => zoneMap[z] === value) ||
                          value;
                        return [label, "Zone"];
                      }}
                    />
                  )}
                  {sysNameChartData.length > 0 && (
                    <LineChartWrapper
                      data={sysNameChartData}
                      xAxisKey="timestamp"
                      lines={[
                        {
                          dataKey: "sysNameNum",
                          stroke: "#3b82f6",
                          type: "stepAfter",
                          dot: false,
                        },
                      ]}
                      yAxisConfig={{
                        type: "number",
                        domain: [0, sysNameCategories.length + 1],
                        ticks: Object.values(sysNameMap),
                        tickFormatter: (v) =>
                          sysNameCategories.find(
                            (name) => sysNameMap[name] === v
                          ) || "",
                        width: 200,
                        tick: { textAnchor: "end" },
                      }}
                      title="SysName History"
                      tooltipFormatter={(_, __, props) => {
                        const value = props.payload.sysNameNum;
                        const label =
                          sysNameCategories.find(
                            (name) => sysNameMap[name] === value
                          ) || value;
                        return [label, "SysName"];
                      }}
                    />
                  )}
                </Suspense>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
