"use client";
import React, { useState, useEffect, useMemo } from "react";

import { Sidebar } from "../components/Sidebar";
import LineChartWrapper from "../components/LineChartWrapper";

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

/**
 * DeviceHistoryChart component visualizes the historical movement and status changes of devices within the network.
 * It fetches device data from a GraphQL endpoint and displays it in line charts.
 * @remarks
 * This component is designed to be used in a client-side context, as it relies on React hooks for state management and side effects.
 * It supports searching for devices by hostname and displays their history in two charts:
 * 1. Zone History: Shows the zone each device was in over time.
 * 2. SysName History: Shows the sysName of each device over time.
 * It also includes a search input with suggestions for device hostnames.
 * @returns The rendered device history chart component.
 */

type DeviceNode = {
  idxDevice: number;
  hostname: string;
  sysName: string;
  zone?: string;
  lastPolled?: number; // UNIX timestamp in seconds
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

export default function DeviceHistoryChart() {
  const [allDevices, setAllDevices] = useState<DeviceNode[]>([]);
  const [inputTerm, setInputTerm] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [range, setRange] = useState("1w");
  const [customStart, setCustomStart] = useState("");
  const [customEnd, setCustomEnd] = useState("");
  const [open, setOpen] = useState(false);

  const now = new Date();
  let startDate: Date | null = null;
  const ranges = [
    { label: "Past 1 day", value: "1d" },
    { label: "Past 1 week", value: "1w" },
    { label: "Past 1 month", value: "1m" },
    { label: "Past 6 months", value: "6m" },
    { label: "Custom range", value: "custom" },
  ];

  useEffect(() => {
    if (range === "custom" && (!customStart || !customEnd)) return;

    let isMounted = true;

    async function fetchDevices() {
      setLoading(true);
      setError(null);
      try {
        const endpoint =
          process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
          "http://localhost:7000/switchmap/api/graphql";
        const res = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: QUERY }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json: GraphQLResponse = await res.json();

        if (json.errors?.length) throw new Error(json.errors[0].message);

        const zones = json.data?.zones?.edges || [];
        let devicesWithZones: DeviceNode[] = [];

        zones.forEach((zoneEdge) => {
          const zone = zoneEdge.node;
          zone.devices.edges.forEach((deviceEdge) => {
            const device = deviceEdge.node;
            if (device?.hostname && device?.idxDevice) {
              devicesWithZones.push({ ...device, zone: zone.name });
            }
          });
        });

        // Time range filtering
        const now = new Date();
        let filteredDevices = devicesWithZones;

        if (range === "custom") {
          const startDate = new Date(customStart!);
          const endDate = new Date(customEnd!);

          filteredDevices = devicesWithZones.filter((d) => {
            if (!d.lastPolled) return false;
            const date = new Date(d.lastPolled * 1000);
            return date >= startDate && date <= endDate;
          });
        } else {
          let startDate: Date | null = null;
          switch (range) {
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
            filteredDevices = devicesWithZones.filter((d) => {
              if (!d.lastPolled) return false;
              const date = new Date(d.lastPolled * 1000);
              return date >= startDate!;
            });
          }
        }

        if (isMounted) {
          setAllDevices(filteredDevices);
          if (filteredDevices.length > 0) {
            setSearchTerm(filteredDevices[0].hostname);
          }
        }
      } catch (err: any) {
        if (isMounted) setError(err.message || "Error fetching devices");
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchDevices();

    return () => {
      isMounted = false;
    };
  }, [range, customStart, customEnd]);

  const uniqueHostnames = useMemo(() => {
    return Array.from(new Set(allDevices.map((d) => d.hostname)));
  }, [allDevices]);

  useEffect(() => {
    if (inputTerm.trim() === "") {
      setSuggestions([]);
      return;
    }
    const filtered = uniqueHostnames
      .filter((host) => host.toLowerCase().includes(inputTerm.toLowerCase()))
      .slice(0, 5);
    setSuggestions(filtered);
  }, [inputTerm, uniqueHostnames]);

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (inputTerm.trim() === "") return;
    setSearchTerm(inputTerm);
    setInputTerm("");
    setSuggestions([]);
  }

  // Sort using lastPolled (converted to ms)
  const history = allDevices
    .filter(
      (d) => d.hostname === searchTerm && typeof d.lastPolled === "number"
    )
    .sort((a, b) => (a.lastPolled ?? 0) * 1000 - (b.lastPolled ?? 0) * 1000);

  // SysName data
  const sysNameCategories = Array.from(new Set(history.map((h) => h.sysName)));
  const sysNameMap: Record<string, number> = {};
  sysNameCategories.forEach((name, i) => {
    sysNameMap[name] = i + 1;
  });
  const sysNameChartData = history.map((h) => ({
    timestamp: new Date((h.lastPolled ?? 0) * 1000).toISOString(),
    sysNameNum: sysNameMap[h.sysName],
    sysName: h.sysName,
  }));

  // Zone data
  const zoneCategories = Array.from(
    new Set(history.map((h) => h.zone || ""))
  ).filter(Boolean);
  const zoneMap: Record<string, number> = {};
  zoneCategories.forEach((zone, i) => {
    zoneMap[zone] = i + 1;
  });
  const zoneChartData = history
    .filter((h) => h.zone)
    .map((h) => ({
      timestamp: new Date((h.lastPolled ?? 0) * 1000).toISOString(),
      zoneNum: zoneMap[h.zone || ""],
      zoneName: h.zone || "",
    }));

  // Fallback UI
  const renderFallback = () => {
    if (loading) {
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <span className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mb-4"></span>
          <p className="text-gray-500">Loading devices...</p>
        </div>
      );
    }
    if (error) {
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-red-600 font-semibold mb-2">Error</p>
          <p className="text-gray-700">{error}</p>
          <button
            className="mt-4 px-4 py-2 rounded bg-blue-600 text-white"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      );
    }
    if (allDevices.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-gray-700">No results found.</p>
        </div>
      );
    }
    if (searchTerm && history.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-gray-700">
            No history found for{" "}
            <span className="font-semibold">{searchTerm}</span>.
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="flex h-screen max-w-full">
      <Sidebar />
      <div className="p-4 w-full max-w-full flex flex-col gap-6 h-full overflow-y-auto mx-10">
        <div className="m-4 md:ml-0">
          <h2 className="text-xl font-semibold">Device History</h2>
          <p className="text-sm pt-2 text-gray-600">
            Visualizing the historical movement and status changes of devices
            within the network.
          </p>
        </div>

        <div className="relative flex flex-col xl:flex-row gap-10 justify-between w-full">
          <form
            className="flex flex-col gap-4 md:flex-row md:items-center"
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
                <ul className="absolute top-full left-0 mt-1 bg-bg shadow-md rounded border w-full z-50 ">
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
              className="border-2 text-button rounded px-4 py-2 cursor-pointer transition-colors duration-300 align-middle h-fit"
              disabled={loading}
            >
              Search
            </button>
          </form>

          <div className="flex flex-col-reverse md:flex-row-reverse xl:flex-row gap-4 text-left justify-end xl:items-center">
            {range === "custom" && (
              <div className="flex flex-col sm:flex-row gap-2 items-start">
                <input
                  type="date"
                  className="border p-2 rounded"
                  value={customStart}
                  onChange={(e) => setCustomStart(e.target.value)}
                />
                <span className="flex items-center justify-center h-full px-2 my-auto">
                  to
                </span>
                <input
                  type="date"
                  className="border p-2 rounded"
                  value={customEnd}
                  onChange={(e) => setCustomEnd(e.target.value)}
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

        <div className="overflow-auto flex-1">
          <div className="gap-8 w-[70vw] min-w-[600px] items-stretch p-4 mx-auto flex flex-col xl:flex-row xl:text-left text-center h-full">
            {renderFallback() || (
              <>
                {/* Zone Chart */}
                {zoneChartData.length > 0 && (
                  <LineChartWrapper
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
                {/* SysName Chart */}
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
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
