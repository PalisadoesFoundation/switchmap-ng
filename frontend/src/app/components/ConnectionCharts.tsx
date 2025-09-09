"use client";
import { useState, useEffect } from "react";
import { FiPlus, FiMinus, FiDownload } from "react-icons/fi";
import HistoricalChart from "./HistoricalChart";
import { DeviceNode } from "../types/graphql/GetZoneDevices";
import { InterfaceNode } from "../types/graphql/GetDeviceInterfaces";

type ChartTab =
  | "Traffic"
  | "Unicast"
  | "NonUnicast"
  | "Errors"
  | "Discards"
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
  devices(hostname: "${hostname}") {
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
  const [expandedIfaces, setExpandedIfaces] = useState<Record<string, boolean>>(
    {}
  );
  const [activeTabs, setActiveTabs] = useState<Record<string, ChartTab>>({});
  const [data, setData] = useState<
    Record<string, Record<ChartTab, ChartDataPoint[]>>
  >({});
  const [error, setError] = useState<string | null>(null);
  // new state
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10; // number of interfaces per page

  // pagination logic
  const totalPages = Math.ceil(device.l1interfaces.edges.length / pageSize);
  const paginatedIfaces = device.l1interfaces.edges.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  // Expand All / Collapse All
  const expandAll = () => {
    const newState = device.l1interfaces.edges.reduce((acc, { node }) => {
      acc[node.ifname] = true;
      return acc;
    }, {} as Record<string, boolean>);
    setExpandedIfaces(newState);
  };

  const collapseAll = () => {
    const newState = device.l1interfaces.edges.reduce((acc, { node }) => {
      acc[node.ifname] = false;
      return acc;
    }, {} as Record<string, boolean>);
    setExpandedIfaces(newState);
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

        const edges = json?.data?.devices?.edges || [];
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

        edges.forEach(({ node }: any) => {
          const lastPolled = new Date(node.lastPolled * 1000);
          if (
            lastPolled < rangeStart ||
            (startDate && lastPolled < new Date(startDate)) ||
            (endDate && lastPolled > new Date(endDate))
          )
            return;

          node.l1interfaces.edges.forEach(({ node: iface }: any) => {
            const ifname = iface.ifname;
            if (!newData[ifname])
              newData[ifname] = {
                Traffic: [],
                Unicast: [],
                NonUnicast: [],
                Errors: [],
                Discards: [],
                Speed: [],
              };

            newData[ifname].Traffic.push({
              lastPolled: lastPolled.toISOString(),
              value: (iface.ifinUcastPkts ?? 0) + (iface.ifoutUcastPkts ?? 0),
            });
            newData[ifname].Unicast.push({
              lastPolled: lastPolled.toISOString(),
              value: (iface.ifinUcastPkts ?? 0) + (iface.ifoutUcastPkts ?? 0),
            });
            newData[ifname].NonUnicast.push({
              lastPolled: lastPolled.toISOString(),
              value: (iface.ifinNUcastPkts ?? 0) + (iface.ifoutNUcastPkts ?? 0),
            });
            newData[ifname].Errors.push({
              lastPolled: lastPolled.toISOString(),
              value: (iface.ifinErrors ?? 0) + (iface.ifoutErrors ?? 0),
            });
            newData[ifname].Discards.push({
              lastPolled: lastPolled.toISOString(),
              value: (iface.ifinDiscards ?? 0) + (iface.ifoutDiscards ?? 0),
            });
            if (iface.ifspeed != null)
              newData[ifname].Speed.push({
                lastPolled: lastPolled.toISOString(),
                value: iface.ifspeed,
              });
          });
        });

        setData(newData);
      } catch (err: any) {
        if (err.name === "AbortError") return;
        setError(err.message);
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

  return (
    <div className="p-8 w-[85vw] flex flex-col gap-6 h-full bg-bg">
      <div className=" min-w-[400px]">
        <h2 className="text-xl font-semibold mb-2">Connection Charts</h2>
        <p className="text-sm">
          View bandwidth, packet flow, errors, and discards per interface.
        </p>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 items-end mb-4">
          <div className="relative w-[160px] items-end">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="appearance-none border rounded px-2 py-1 w-full bg-bg pr-6 "
            >
              <option value="24h">Past 24 hours</option>
              <option value="7d">Past 7 days</option>
              <option value="30d">Past 30 days</option>
              <option value="custom">Custom Date</option>
            </select>

            <div className="pointer-events-none absolute inset-y-0 right-2 flex items-center">
              <svg
                className="h-5 w-5 text-gray-500"
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
            </div>
          </div>

          <div className="min-h-[60px] flex gap-4 items-end">
            {timeRange === "custom" && (
              <>
                <div>
                  <label className="text-sm block mb-1">Start Date</label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="border rounded px-2 py-1 bg-bg"
                  />
                </div>
                <div>
                  <label className="text-sm block mb-1">End Date</label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="border rounded px-2 py-1 bg-bg"
                  />
                </div>
              </>
            )}
          </div>

          <div className="flex gap-4 sm:ml-auto mr-0 align-bottom">
            <button
              className="inline-flex justify-between items-center bg-bg px-4 py-2 border border-gray-300 rounded-md shadow-sm outline"
              onClick={expandAll}
            >
              Expand All
            </button>
            <button
              className="inline-flex justify-between items-center bg-bg px-4 py-2 border border-gray-300 rounded-md shadow-sm outline"
              onClick={collapseAll}
            >
              Collapse All
            </button>
          </div>
        </div>

        {/* Interfaces with Pagination */}
        <div className="flex flex-col gap-4">
          {paginatedIfaces.map(({ node }: { node: InterfaceNode }) => {
            const ifname = node.ifname;
            const isExpanded = expandedIfaces[ifname];
            const currentTab = activeTabs[ifname] || "Traffic";
            const filteredData = data[ifname]?.[currentTab] || [];

            return (
              <div
                key={ifname}
                className="border rounded-lg p-2 bg-content-bg shadow-md relative mb-2"
              >
                <div
                  className="flex items-center gap-2 cursor-pointer ml-2"
                  onClick={() =>
                    setExpandedIfaces((prev) => ({
                      ...prev,
                      [ifname]: !prev[ifname],
                    }))
                  }
                >
                  {isExpanded ? <FiMinus /> : <FiPlus />}
                  <p className="font-medium">{ifname}</p>
                </div>

                {isExpanded && (
                  <>
                    <div className="flex gap-6 border-b border-border-subtle mt-4 mb-4">
                      <button
                        className="absolute top-2 right-2 md:top-4 md:right-4 px-3 py-1 md:py-2 rounded-md shadow-sm text-white"
                        style={{ backgroundColor: "#CB3CFF" }}
                        onClick={() =>
                          downloadCSV(
                            filteredData,
                            `${ifname}-${currentTab}.csv`
                          )
                        }
                      >
                        <FiDownload className="inline mr-1" /> Download
                      </button>
                      {(
                        [
                          "Traffic",
                          "Unicast",
                          "NonUnicast",
                          "Errors",
                          "Discards",
                          "Speed",
                        ] as ChartTab[]
                      ).map((tab) => (
                        <button
                          key={tab}
                          className={`pb-2 text-sm font-medium transition-colors duration-150 ${
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
                          {tab}
                        </button>
                      ))}
                    </div>

                    {filteredData.length > 0 ? (
                      <div className="relative  min-h-[300px] mr-2">
                        <HistoricalChart
                          data={filteredData}
                          title={`${ifname} - ${currentTab}`}
                          color={
                            currentTab === "Traffic"
                              ? "#8884d8"
                              : currentTab === "Speed"
                              ? "#FF5733"
                              : "#82ca9d"
                          }
                          unit={currentTab === "Speed" ? " Mbps" : " pkts"}
                        />
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

          {/* Pagination Controls */}
          <div className="flex justify-center gap-4 mt-4 mb-4">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => p - 1)}
              className="px-3 py-1 border rounded disabled:opacity-50"
            >
              Previous
            </button>
            <span className="text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => p + 1)}
              className="px-3 py-1 border rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
