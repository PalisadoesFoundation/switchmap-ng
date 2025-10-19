"use client";
import React, {
  useEffect,
  useMemo,
  useState,
  useCallback,
  Suspense,
} from "react";
import { DeviceNode } from "../types/graphql/GetZoneDevices";
import styles from "./DeviceDetails.module.css";
import { formatUptime } from "../utils/time";
import { formatUnixTimestamp } from "../utils/timeStamp";
import { truncateLines } from "../utils/stringUtils";
const HistoricalChart = React.lazy(() => import("./HistoricalChart"));
const TopologyChart = React.lazy(() =>
  import("./TopologyChart").then((m) => ({ default: m.TopologyChart }))
);

/**
 * DeviceDetails component displays detailed information about a specific device.
 *
 * @remarks
 * This component shows metadata about the device, including its name, description,
 * hostname, status, uptime, system ID, and last polled time. It also includes
 * historical charts for system status, CPU usage, and memory usage. The component
 * allows users to filter the historical data by predefined time ranges or a custom range.
 * @param device - The device object containing its details.
 * @returns The DeviceDetails component.
 *
 * @see {@link HistoricalChart} for displaying historical data charts.
 * @see {@link TopologyChart} for displaying the device in a network topology.
 */

function MetadataRow({ label, value }: { label: string; value: string }) {
  return (
    <tr>
      <th className="py-2 pr-4 w-40">{label}</th>
      <td className="py-2">{value}</td>
    </tr>
  );
}

type DeviceData = {
  hostname: string;
  sysUptime?: number;
  cpuUtilization: number;
  memoryUtilization: number;
  lastPolled: number;
  sysName?: string;
  sysDescription?: string;
  sysObjectid?: string;
};

type SystemStatNode = {
  idxSystemstat: string;
  cpu5min: string | number;
  memUsed: string | number;
  memFree: string | number;
};

type SystemStatEdge = {
  node: SystemStatNode;
};

type DeviceGraphQLNode = {
  id: string;
  hostname: string;
  lastPolled: number;
  sysUptime?: number;
  systemstats?: {
    edges: SystemStatEdge[];
  };
};

type DeviceEdge = {
  node: DeviceGraphQLNode;
};

export type DeviceDetailsProps = {
  device: DeviceNode;
};

const TIME_RANGES = [
  { label: "Past 1 day", value: 1 },
  { label: "Past 1 week", value: 7 },
  { label: "Past 1 month", value: 30 },
  { label: "Past 6 months", value: 180 },
  { label: "Custom range", value: 0 },
];

export function DeviceDetails({ device }: DeviceDetailsProps) {
  const [uptimeData, setUptimeData] = useState<
    { lastPolled: string; value: number }[]
  >([]);
  const [cpuUsageData, setCpuUsageData] = useState<
    { lastPolled: string; value: number }[]
  >([]);
  const [memoryUsageData, setMemoryUsageData] = useState<
    { lastPolled: string; value: number }[]
  >([]);
  const [deviceMetrics, setDeviceMetrics] = useState<DeviceData | null>(null);
  const [selectedRange, setSelectedRange] = useState<number>(1);
  const [customRange, setCustomRange] = useState<{
    start: string;
    end: string;
  }>({ start: "", end: "" });
  const [errorMsg, setErrorMsg] = useState("");
  const [open, setOpen] = useState(false);

  const topologyChartMemo = useMemo(
    () => (
      <Suspense
        fallback={
          <div className="text-center text-gray-400 py-4">Loading chart...</div>
        }
      >
        <TopologyChart
          devices={[device]}
          loading={false}
          error={null}
          zoomView={false}
          clickToUse={false}
        />
      </Suspense>
    ),
    [device]
  );

  const metadataTableMemo = useMemo(
    () => (
      <div className="max-w-full min-h-[350px] h-auto min-w-[300px] w-auto md:w-[50vw] p-5 mx-4 bg-content-bg border border-border-subtle rounded-lg xl:w-[35vw]">
        <table
          className={`table-auto w-fit m-top-0 text-left ${styles.tableCustom}`}
        >
          <tbody className="text-xs md:text-sm xl:text-lg">
            <MetadataRow label="Device Name" value={device.sysName ?? "-"} />
            <MetadataRow
              label="Description"
              value={truncateLines(device.sysDescription ?? "", {
                lines: 3,
                maxLength: 60,
              })}
            />
            <MetadataRow label="Hostname" value={device.hostname} />
            <MetadataRow
              label="Status"
              value={device.sysUptime && device.sysUptime > 0 ? "Up" : "Down"}
            />
            <MetadataRow
              label="Uptime"
              value={formatUptime(
                device.sysUptime ?? (deviceMetrics?.sysUptime ?? 0) * 100
              )}
            />
            <MetadataRow label="System ID" value={device.sysObjectid ?? "-"} />
            <MetadataRow
              label="Time Last Polled"
              value={formatUnixTimestamp(
                deviceMetrics?.lastPolled ?? device.lastPolled
              )}
            />
          </tbody>
        </table>
      </div>
    ),
    [device, deviceMetrics]
  );

  const query = `
query SystemStats($hostname: String!) {
  deviceByHostname(hostname: $hostname) {
    edges {
      node {
        id
        hostname
        lastPolled
        sysUptime
        systemstats {
          edges {
            node {
              idxSystemstat
              cpu5min
              memUsed
              memFree
            }
          }
        }
      }
    }
  }
}
`;

  useEffect(() => {
    const ac = new AbortController();
    async function fetchData() {
      try {
        const res = await fetch(
          process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              query,
              variables: { hostname: device.hostname },
            }),
            signal: ac.signal,
          }
        );
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (json?.errors?.length)
          throw new Error(json.errors[0]?.message || "GraphQL error");

        const deviceEdges = json.data.deviceByHostname?.edges;

        if (!deviceEdges || deviceEdges.length === 0)
          throw new Error("No devices found");

        const hostMetrics: DeviceData[] = [];

        deviceEdges.forEach(({ node: deviceData }: DeviceEdge) => {
          if (deviceData.hostname !== device.hostname) {
            return;
          }

          if (deviceData?.systemstats?.edges) {
            deviceData.systemstats.edges.forEach(
              ({ node: statNode }: SystemStatEdge) => {
                hostMetrics.push({
                  hostname: deviceData.hostname,
                  sysUptime: deviceData.sysUptime,
                  cpuUtilization: (() => {
                    const raw = Number(statNode.cpu5min ?? 0);
                    return Number.isFinite(raw) ? raw : 0;
                  })(),
                  memoryUtilization: (() => {
                    const used = Number(statNode.memUsed ?? 0);
                    const free = Number(statNode.memFree ?? 0);
                    const total = used + free;
                    if (
                      !Number.isFinite(used) ||
                      !Number.isFinite(free) ||
                      total <= 0
                    ) {
                      return 0;
                    }
                    return (used / total) * 100;
                  })(),
                  lastPolled: Number(deviceData.lastPolled),
                  sysName: undefined,
                  sysDescription: undefined,
                  sysObjectid: undefined,
                });
              }
            );
          }
        });

        hostMetrics.sort((a, b) => a.lastPolled - b.lastPolled);

        if (!hostMetrics.length) {
          setUptimeData([]);
          setCpuUsageData([]);
          setMemoryUsageData([]);
          setDeviceMetrics(null);
          return;
        }

        setDeviceMetrics(hostMetrics[hostMetrics.length - 1]);

        setUptimeData(
          hostMetrics.map((m) => ({
            lastPolled: new Date(m.lastPolled * 1000).toISOString(),
            value: m.sysUptime && m.sysUptime > 0 ? 1 : 0,
          }))
        );

        setCpuUsageData(
          hostMetrics.map((m) => ({
            lastPolled: new Date(m.lastPolled * 1000).toISOString(),
            value: Math.max(0, Math.min(100, Number(m.cpuUtilization))),
          }))
        );

        setMemoryUsageData(
          hostMetrics.map((m) => ({
            lastPolled: new Date(m.lastPolled * 1000).toISOString(),
            value: Math.max(0, Math.min(100, Number(m.memoryUtilization))),
          }))
        );
      } catch (error: unknown) {
        if (error instanceof Error && error.name === "AbortError") return;
        console.error("Error fetching device metrics:", error);
        setErrorMsg("Failed to load device metrics.");
        setTimeout(() => setErrorMsg(""), 3000);
      }
    }
    fetchData();
    return () => ac.abort();
  }, [device.hostname, query]);

  const filterByRange = useCallback(
    (data: { lastPolled: string; value: number }[]) => {
      const now = new Date();
      let startDate: Date;
      if (selectedRange === 0 && customRange.start && customRange.end) {
        startDate = new Date(customRange.start);
        startDate.setHours(0, 0, 0, 0);
        const endDate = new Date(customRange.end);
        endDate.setHours(23, 59, 59, 999);
        return data.filter(
          (d) =>
            new Date(d.lastPolled) >= startDate &&
            new Date(d.lastPolled) <= endDate
        );
      } else {
        startDate = new Date();
        startDate.setDate(now.getDate() - selectedRange);
        return data.filter((d) => new Date(d.lastPolled) >= startDate);
      }
    },
    [selectedRange, customRange]
  );

  const filteredUptime = useMemo(
    () => filterByRange(uptimeData),
    [filterByRange, uptimeData]
  );
  const filteredCpu = useMemo(
    () => filterByRange(cpuUsageData),
    [filterByRange, cpuUsageData]
  );
  const filteredMemory = useMemo(
    () => filterByRange(memoryUsageData),
    [filterByRange, memoryUsageData]
  );

  return (
    <div className="p-8 w-[80vw] flex flex-col gap-4 h-full">
      {errorMsg && (
        <div className="fixed inset-0 flex mt-2 items-start justify-center z-50 pointer-events-none">
          <div className="bg-gray-300 text-gray-900 px-6 py-3 rounded shadow-lg animate-fade-in pointer-events-auto">
            {errorMsg}
          </div>
        </div>
      )}

      <h2 className="text-xl font-semibold mb-2">Device Overview</h2>
      <div
        className={`flex flex-col md:flex-row md:self-center gap-2 h-fit ${styles.deviceChartWrapper}`}
      >
        {topologyChartMemo}
        {metadataTableMemo}
      </div>
      {/* Time Range Dropdown */}
      <div className="mt-8 md:mt-2 flex flex-col lg:flex-row gap-4 text-left justify-start xl:items-center">
        <div className="relative">
          <button
            type="button"
            className="flex justify-between items-center border rounded px-4 py-2 w-48"
            onClick={() => setOpen(!open)}
          >
            {TIME_RANGES.find((r) => r.value === selectedRange)?.label}
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
              {TIME_RANGES.map((r) => (
                <button
                  key={r.value}
                  className="w-full text-left px-4 py-2 hover:bg-hover-bg"
                  onClick={() => {
                    setSelectedRange(r.value);
                    setOpen(false);
                  }}
                >
                  {r.label}
                </button>
              ))}
            </div>
          )}
        </div>
        {selectedRange === 0 && (
          <div className="flex flex-col lg:flex-row gap-8 items-start">
            <label className="flex flex-col lg:flex-row gap-2 lg:items-center">
              Start date{" "}
              <input
                type="date"
                className="border p-2 rounded"
                value={customRange.start}
                onChange={(e) => {
                  const start = new Date(e.target.value);
                  const end = customRange.end
                    ? new Date(customRange.end)
                    : null;
                  if (end && start > end) {
                    setErrorMsg("Start date must be before end date.");
                    setTimeout(() => setErrorMsg(""), 3000);
                    return;
                  }
                  if (
                    end &&
                    (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24) >
                      180
                  ) {
                    setErrorMsg("Custom range cannot exceed 180 days.");
                    setTimeout(() => setErrorMsg(""), 3000);
                    return;
                  }

                  setCustomRange({ ...customRange, start: e.target.value });
                }}
              />
            </label>
            <label className="flex flex-col lg:flex-row gap-2 lg:items-center">
              End date{" "}
              <input
                type="date"
                className="border p-2 rounded"
                value={customRange.end}
                onChange={(e) => {
                  const start = customRange.start
                    ? new Date(customRange.start)
                    : null;
                  const end = new Date(e.target.value);
                  if (start && end < start) {
                    setErrorMsg("End date must be after start date.");
                    setTimeout(() => setErrorMsg(""), 3000);
                    return;
                  }

                  if (
                    start &&
                    end &&
                    (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24) >
                      180
                  ) {
                    setErrorMsg("Custom range cannot exceed 180 days.");
                    setTimeout(() => setErrorMsg(""), 3000);
                    return;
                  }

                  setCustomRange({ ...customRange, end: e.target.value });
                }}
              />
            </label>
          </div>
        )}
      </div>

      <div className="p-4 w-full min-w-[350px] flex flex-col xl:flex-row gap-4">
        {filteredUptime?.length ? (
          <Suspense
            fallback={
              <div className="text-center text-gray-400 py-4">
                Loading chart...
              </div>
            }
          >
            <HistoricalChart
              title="System Status"
              data={filteredUptime}
              color="#00b894"
              unit=""
              yAxisConfig={{
                domain: [0, 1],
                ticks: [0, 1],
                tickFormatter: (v) => (v === 1 ? "Up" : "Down"),
                allowDecimals: false,
              }}
              lineType="stepAfter"
            />
          </Suspense>
        ) : (
          <div className="flex items-center justify-center w-full h-64 rounded-xl border text-gray-500">
            No uptime data available
          </div>
        )}

        {filteredCpu?.length ? (
          <Suspense
            fallback={
              <div className="text-center text-gray-400 py-4">
                Loading chart...
              </div>
            }
          >
            <HistoricalChart
              title="CPU Usage (%)"
              data={filteredCpu}
              color="#0984e3"
              unit="%"
            />
          </Suspense>
        ) : (
          <div className="flex items-center justify-center w-full h-64 rounded-xl border text-gray-500">
            No CPU data available
          </div>
        )}

        {filteredMemory?.length ? (
          <Suspense
            fallback={
              <div className="text-center text-gray-400 py-4">
                Loading chart...
              </div>
            }
          >
            <HistoricalChart
              title="Memory Usage (%)"
              data={filteredMemory}
              color="#e17055"
              unit="%"
            />
          </Suspense>
        ) : (
          <div className="flex items-center justify-center w-full h-64 rounded-xl border text-gray-500">
            No memory data available
          </div>
        )}
      </div>
    </div>
  );
}
