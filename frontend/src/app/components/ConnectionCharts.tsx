"use client";
import { useState, useEffect, useMemo } from "react";
import { FiPlus, FiMinus, FiDownload } from "react-icons/fi";
import HistoricalChart from "./HistoricalChart";
import { DeviceNode } from "../types/graphql/GetZoneDevices";
import { InterfaceNode } from "../types/graphql/GetDeviceInterfaces";
/**
 * ConnectionCharts component displays historical charts for a device's network interfaces.
 *
 * @remarks
 * This component allows users to view historical data for various metrics related to network interfaces.
 * Users can select different time ranges, expand/collapse interface sections, and switch between different chart types.
 * The component fetches data from a GraphQL endpoint and renders charts using the HistoricalChart component.
 * @see {@link HistoricalChart} for rendering the charts.
 * @see {@link useState}, {@link useEffect}, {@link useMemo} for React hooks used in the component.
 * @see {@link DeviceNode}, {@link InterfaceNode} for the types used in the component.
 */

type ChartTab =
  | "TrafficIn"
  | "TrafficOut"
  | "UnicastIn"
  | "UnicastOut"
  | "NonUnicastIn"
  | "NonUnicastOut"
  | "ErrorsTotal"
  | "DiscardsTotal"
  | "Speed";

interface ChartDataPoint {
  lastPolled: string;
  value: number;
}

interface ConnectionChartsProps {
  device: DeviceNode;
}

const QUERY = (hostname: string) => `
{
  deviceByHostname(hostname: "${hostname}") {
    edges {
      node {
        id
        hostname
        sysName
        lastPolled
        l1interfaces {
          edges {
            node {
              ifname
              ifspeed
              ifinOctets
              ifoutOctets
              ifinUcastPkts
              ifoutUcastPkts
              ifinNucastPkts
              ifoutNucastPkts
              ifinErrors
              ifoutErrors
              ifinDiscards
              ifoutDiscards
            }
          }
        }
      }
    }
  }
}
`;

export function ConnectionCharts({ device }: ConnectionChartsProps) {
  const [timeRange, setTimeRange] = useState("24h");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [expandedIfaces, setExpandedIfaces] = useState<
    Record<number, Record<string, boolean>>
  >({});
  const [activeTabs, setActiveTabs] = useState<Record<string, ChartTab>>({});
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [data, setData] = useState<
    Record<string, Record<ChartTab, ChartDataPoint[]>>
  >({});
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  const totalPages = Math.max(
    1,
    Math.ceil(device.l1interfaces.edges.length / pageSize)
  );
  const paginatedIfaces = useMemo(
    () =>
      device.l1interfaces.edges.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
      ),
    [device.l1interfaces.edges, currentPage]
  );
  useEffect(() => {
    setCurrentPage((prev) => Math.min(Math.max(prev, 1), totalPages));
  }, [totalPages]);

  const TIME_RANGES = [
    { value: "24h", label: "Past 1 day" },
    { value: "7d", label: "Past 7 days" },
    { value: "30d", label: "Past 30 days" },
    { value: "custom", label: "Custom range" },
  ];

  const expandAll = () => {
    const newState = device.l1interfaces.edges
      .slice((currentPage - 1) * pageSize, currentPage * pageSize)
      .reduce((acc, { node }) => {
        acc[node.ifname] = true;
        return acc;
      }, {} as Record<string, boolean>);

    setExpandedIfaces((prev) => ({
      ...prev,
      [currentPage]: newState,
    }));
  };

  const collapseAll = () => {
    const newState = device.l1interfaces.edges
      .slice((currentPage - 1) * pageSize, currentPage * pageSize)
      .reduce((acc, { node }) => {
        acc[node.ifname] = false;
        return acc;
      }, {} as Record<string, boolean>);

    setExpandedIfaces((prev) => ({
      ...prev,
      [currentPage]: newState,
    }));
  };

  useEffect(() => {
    const ac = new AbortController();
    let cancelled = false;

    const fetchData = async () => {
      try {
        const res = await fetch(
          process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: QUERY(device.hostname) }),
            signal: ac.signal,
          }
        );

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const json = await res.json();
        if (cancelled) return;

        const edges = json?.data?.deviceByHostname?.edges || [];
        const newData: Record<string, Record<ChartTab, ChartDataPoint[]>> = {};
        const now = new Date();
        let rangeStart: Date;

        if (timeRange === "24h")
          rangeStart = new Date(now.getTime() - 24 * 3600 * 1000);
        else if (timeRange === "7d")
          rangeStart = new Date(now.getTime() - 7 * 24 * 3600 * 1000);
        else if (timeRange === "30d")
          rangeStart = new Date(now.getTime() - 30 * 24 * 3600 * 1000);
        else rangeStart = new Date(0);

        // Helpers: local day bounds and precomputed ms thresholds
        const dayBounds = (dateStr: string) => {
          const [y, m, d] = dateStr.split("-").map(Number);
          if (!y || !m || !d) return [undefined, undefined] as const;
          return [
            new Date(y, m - 1, d, 0, 0, 0, 0).getTime(),
            new Date(y, m - 1, d, 23, 59, 59, 999).getTime(),
          ] as const;
        };
        const [startMsBound] = startDate ? dayBounds(startDate) : [undefined];
        const [, endMsBound] = endDate
          ? dayBounds(endDate)
          : [undefined, undefined];
        const rangeStartMs = rangeStart.getTime();

        edges.forEach(
          ({
            node,
          }: {
            node: Partial<DeviceNode> & {
              lastPolled: number | string;
              l1interfaces: { edges: { node: InterfaceNode }[] };
            };
          }) => {
            const lp = node.lastPolled as number | string;
            const ms =
              typeof lp === "number"
                ? lp < 1e12
                  ? lp * 1000
                  : lp
                : Date.parse(lp);
            if (Number.isNaN(ms)) return;
            const lastPolled = new Date(ms);
            if (
              ms < rangeStartMs ||
              (startMsBound !== undefined && ms < startMsBound) ||
              (endMsBound !== undefined && ms > endMsBound)
            )
              return;

            node.l1interfaces.edges.forEach(
              ({ node: iface }: { node: InterfaceNode }) => {
                const ifname = iface.ifname;
                if (!newData[ifname])
                  newData[ifname] = {
                    TrafficIn: [],
                    TrafficOut: [],
                    UnicastIn: [],
                    UnicastOut: [],
                    NonUnicastIn: [],
                    NonUnicastOut: [],
                    ErrorsTotal: [],
                    DiscardsTotal: [],
                    Speed: [],
                  };

                // Traffic data - separate input and output
                if (iface.ifinOctets != null) {
                  newData[ifname].TrafficIn.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifinOctets,
                  });
                }

                if (iface.ifoutOctets != null) {
                  newData[ifname].TrafficOut.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifoutOctets,
                  });
                }

                // Unicast packets data - separate input and output
                if (iface.ifinUcastPkts != null) {
                  newData[ifname].UnicastIn.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifinUcastPkts,
                  });
                }

                if (iface.ifoutUcastPkts != null) {
                  newData[ifname].UnicastOut.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifoutUcastPkts,
                  });
                }

                // Non-unicast packets data - separate input and output
                if (iface.ifinNucastPkts != null) {
                  newData[ifname].NonUnicastIn.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifinNucastPkts,
                  });
                }

                if (iface.ifoutNucastPkts != null) {
                  newData[ifname].NonUnicastOut.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifoutNucastPkts,
                  });
                }

                // Errors data - total makes sense here
                if (iface.ifinErrors != null || iface.ifoutErrors != null) {
                  newData[ifname].ErrorsTotal.push({
                    lastPolled: lastPolled.toISOString(),
                    value: (iface.ifinErrors ?? 0) + (iface.ifoutErrors ?? 0),
                  });
                }

                // Discards data - total makes sense here
                if (iface.ifinDiscards != null || iface.ifoutDiscards != null) {
                  newData[ifname].DiscardsTotal.push({
                    lastPolled: lastPolled.toISOString(),
                    value:
                      (iface.ifinDiscards ?? 0) + (iface.ifoutDiscards ?? 0),
                  });
                }

                // Speed data
                if (iface.ifspeed != null) {
                  newData[ifname].Speed.push({
                    lastPolled: lastPolled.toISOString(),
                    value: iface.ifspeed,
                  });
                }
              }
            );
          }
        );

        // Sort all data arrays chronologically by lastPolled timestamp
        Object.keys(newData).forEach((ifname) => {
          Object.keys(newData[ifname]).forEach((chartType) => {
            newData[ifname][chartType as ChartTab].sort(
              (a, b) =>
                new Date(a.lastPolled).getTime() -
                new Date(b.lastPolled).getTime()
            );
          });
        });

        setData(newData);
      } catch (err: unknown) {
        if (err instanceof Error) {
          if (err.name === "AbortError") return;
          setError(err.message);
        } else {
          // handle non-Error cases if needed
          setError(String(err));
        }
      }
    };

    fetchData();
    return () => {
      cancelled = true;
      ac.abort();
    };
  }, [device.hostname, timeRange, startDate, endDate]);

  const downloadCSV = (data: ChartDataPoint[], filename: string) => {
    const csv = [
      "lastPolled,value",
      ...data.map((p) => `${p.lastPolled},${p.value}`),
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getTabDisplayName = (tab: ChartTab): string => {
    switch (tab) {
      case "TrafficIn":
        return "Traffic In";
      case "TrafficOut":
        return "Traffic Out";
      case "UnicastIn":
        return "Unicast In";
      case "UnicastOut":
        return "Unicast Out";
      case "NonUnicastIn":
        return "Non-Unicast In";
      case "NonUnicastOut":
        return "Non-Unicast Out";
      case "ErrorsTotal":
        return "Total Errors";
      case "DiscardsTotal":
        return "Total Discards";
      case "Speed":
        return "Speed";
      default:
        return tab;
    }
  };

  const formatLargeNumber = (value: number): string => {
    if (value >= 1e9) {
      return (value / 1e9).toFixed(1) + "G";
    } else if (value >= 1e6) {
      return (value / 1e6).toFixed(1) + "M";
    } else if (value >= 1e3) {
      return (value / 1e3).toFixed(1) + "K";
    }
    return value.toString();
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 w-full max-w-7xl mx-auto flex flex-col gap-6 h-full bg-bg">
      {error && (
        <div className="fixed inset-0 flex mt-2 items-start justify-center z-50 pointer-events-none">
          <div className="bg-gray-300 text-gray-900 px-6 py-3 rounded shadow-lg animate-fade-in pointer-events-auto">
            {error}
          </div>
        </div>
      )}
      <div className="min-w-0 w-full">
        <h2 className="text-xl font-semibold mb-2">Connection Charts</h2>
        <p className="text-sm">
          View bandwidth, packet flow, errors, and discards per interface.
        </p>

        <div className="flex flex-col sm:flex-row flex-wrap gap-4 items-start sm:items-end mb-4 mt-4">
          <div className="relative w-full sm:w-[160px]">
            <button
              type="button"
              className="flex justify-between items-end w-full border border-gray-300 rounded px-3 py-1 bg-bg transition-colors"
              onClick={() => setDropdownOpen(!dropdownOpen)}
            >
              {TIME_RANGES.find((r) => r.value === timeRange)?.label ||
                "Select Range"}
              <svg
                className={`ml-2 h-5 w-5 text-gray-500 transition-transform ${
                  dropdownOpen ? "rotate-180" : ""
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

            {dropdownOpen && (
              <div className="absolute mt-1 w-full bg-bg border border-gray-300 rounded shadow z-10">
                {TIME_RANGES.map((r) => (
                  <button
                    key={r.value}
                    className="w-full text-left px-3 py-2 hover:bg-hover-bg transition-colors"
                    onClick={() => {
                      setTimeRange(r.value);
                      setDropdownOpen(false);
                    }}
                  >
                    {r.label}
                  </button>
                ))}
              </div>
            )}
          </div>

          {timeRange === "custom" && (
            <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-end w-full sm:w-auto">
              <div className="w-full sm:w-auto">
                <label htmlFor="startDate" className="text-sm block mb-1">
                  Start Date
                </label>
                <input
                  id="startDate"
                  type="date"
                  value={startDate}
                  onChange={(e) => {
                    const start = new Date(e.target.value);
                    const end = endDate ? new Date(endDate) : null;

                    if (end && start > end) {
                      setError("Start date must be before end date.");
                      setTimeout(() => setError(""), 3000);
                      return;
                    }

                    if (
                      end &&
                      (end.getTime() - start.getTime()) /
                        (1000 * 60 * 60 * 24) >
                        180
                    ) {
                      setError("Custom range cannot exceed 180 days.");
                      setTimeout(() => setError(""), 3000);
                      return;
                    }

                    setStartDate(e.target.value);
                  }}
                  className="border border-gray-300 rounded px-2 py-1 bg-bg w-full sm:w-auto"
                />
              </div>
              <div className="w-full sm:w-auto">
                <label htmlFor="endDate" className="text-sm block mb-1">
                  End Date
                </label>
                <input
                  id="endDate"
                  type="date"
                  value={endDate}
                  onChange={(e) => {
                    const end = new Date(e.target.value);
                    const start = startDate ? new Date(startDate) : null;

                    if (start && end < start) {
                      setError("End date must be after start date.");
                      setTimeout(() => setError(""), 3000);
                      return;
                    }

                    if (
                      start &&
                      (end.getTime() - start.getTime()) /
                        (1000 * 60 * 60 * 24) >
                        180
                    ) {
                      setError("Custom range cannot exceed 180 days.");
                      setTimeout(() => setError(""), 3000);
                      return;
                    }

                    setEndDate(e.target.value);
                  }}
                  className="border border-gray-300 rounded px-2 py-1 bg-bg w-full sm:w-auto"
                />
              </div>
            </div>
          )}

          <div className="flex gap-2 sm:gap-4 w-full sm:w-auto sm:ml-auto justify-start sm:justify-end">
            <button
              className="inline-flex justify-center items-center bg-bg px-3 sm:px-4 py-2 border border-gray-300 rounded-md shadow-sm hover:border-gray-400 transition-colors text-sm"
              onClick={expandAll}
            >
              Expand All
            </button>
            <button
              className="inline-flex justify-center items-center bg-bg px-3 sm:px-4 py-2 border border-gray-300 rounded-md shadow-sm hover:border-gray-400 transition-colors text-sm"
              onClick={collapseAll}
            >
              Collapse All
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-4 mx-1 sm:mx-2">
          {paginatedIfaces.map(({ node }: { node: InterfaceNode }) => {
            const ifname = node.ifname;
            const currentPageState = expandedIfaces[currentPage] || {};
            const isExpanded = currentPageState[ifname] || false;
            const currentTab = activeTabs[ifname] || "TrafficIn";
            const filteredData = data[ifname]?.[currentTab] || [];

            return (
              <div
                key={ifname}
                className="border border-gray-300 rounded-lg p-2 sm:p-3 lg:p-4 bg-content-bg relative mb-2"
              >
                <div className="flex items-center justify-between">
                  <div
                    className="flex items-center gap-2 cursor-pointer ml-2"
                    onClick={() =>
                      setExpandedIfaces((prev) => ({
                        ...prev,
                        [currentPage]: {
                          ...(prev[currentPage] || {}),
                          [ifname]: !(prev[currentPage] || {})[ifname],
                        },
                      }))
                    }
                  >
                    {isExpanded ? <FiMinus /> : <FiPlus />}
                    <p className="font-medium">{ifname}</p>
                  </div>

                  {isExpanded && (
                    <button
                      className="px-2 py-1 rounded text-white bg-primary text-xs hover:bg-primary/90 transition-colors flex items-center gap-1"
                      onClick={() =>
                        downloadCSV(filteredData, `${ifname}-${currentTab}.csv`)
                      }
                    >
                      <FiDownload className="w-3 h-3" />
                      <span className="hidden sm:inline">CSV</span>
                    </button>
                  )}
                </div>

                {isExpanded && (
                  <>
                    <div className="mt-4 mb-4">
                      <div className="w-full">
                        <div className="w-full overflow-x-auto overflow-y-hidden tab-scrollbar">
                          <div className="flex gap-2 sm:gap-4 lg:gap-6 border-b border-border-subtle pb-2 min-w-max">
                            {(
                              [
                                "TrafficIn",
                                "TrafficOut",
                                "UnicastIn",
                                "UnicastOut",
                                "NonUnicastIn",
                                "NonUnicastOut",
                                "ErrorsTotal",
                                "DiscardsTotal",
                                "Speed",
                              ] as ChartTab[]
                            ).map((tab) => (
                              <button
                                key={tab}
                                className={`pb-2 text-xs sm:text-sm font-medium transition-colors duration-150 whitespace-nowrap flex-shrink-0 ${
                                  currentTab === tab
                                    ? "border-b-2 border-primary text-primary"
                                    : "text-gray-500 hover:text-primary"
                                }`}
                                onClick={() =>
                                  setActiveTabs((prev) => ({
                                    ...prev,
                                    [ifname]: tab,
                                  }))
                                }
                              >
                                {getTabDisplayName(tab)}
                              </button>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>

                    {filteredData.length > 0 ? (
                      <div className="w-full">
                        <div className="relative min-h-[250px] sm:min-h-[300px] lg:min-h-[400px] w-full max-w-full overflow-hidden border border-gray-200 rounded-lg bg-bg">
                          <div className="absolute inset-0 p-2 sm:p-4">
                            <HistoricalChart
                              data={filteredData}
                              title={`${ifname} - ${getTabDisplayName(
                                currentTab
                              )}`}
                              color={
                                currentTab.startsWith("Traffic")
                                  ? "#8884d8"
                                  : currentTab === "Speed"
                                  ? "#FF5733"
                                  : currentTab.startsWith("Unicast")
                                  ? "#82ca9d"
                                  : currentTab.startsWith("NonUnicast")
                                  ? "#ffc658"
                                  : currentTab.includes("Errors")
                                  ? "#ff7300"
                                  : currentTab.includes("Discards")
                                  ? "#ff0000"
                                  : "#82ca9d"
                              }
                              unit={
                                currentTab === "Speed"
                                  ? " Mbps"
                                  : currentTab.startsWith("Traffic")
                                  ? " octets"
                                  : currentTab.includes("Errors") ||
                                    currentTab.includes("Discards")
                                  ? " errors"
                                  : " pkts"
                              }
                              yAxisConfig={
                                currentTab.startsWith("Traffic") ||
                                currentTab.startsWith("Unicast") ||
                                currentTab.startsWith("NonUnicast")
                                  ? {
                                      tickFormatter: formatLargeNumber,
                                      allowDecimals: false,
                                    }
                                  : undefined
                              }
                            />
                          </div>
                        </div>
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500 mt-4">
                        No data available for the selected range.
                      </p>
                    )}
                  </>
                )}
              </div>
            );
          })}

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 mt-4 mb-4">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => p - 1)}
              className="px-4 py-2 border rounded disabled:opacity-50 hover:bg-gray-50 transition-colors w-full sm:w-auto"
            >
              Previous
            </button>
            <span className="text-sm text-center">
              Page {currentPage} of {totalPages}
            </span>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => p + 1)}
              className="px-4 py-2 border rounded disabled:opacity-50 hover:bg-gray-50 transition-colors w-full sm:w-auto"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
