import React, { useEffect, useMemo, useState } from "react";
import HistoricalChart from "./HistoricalChart";
import { TopologyChart } from "./TopologyChart";
import { DeviceNode } from "../types/graphql/GetZoneDevices";
import styles from "./DeviceDetails.module.css";
import { formatUptime } from "../utils/time";
import { formatUnixTimestamp } from "../utils/timeStamp";
import { truncateLines } from "../utils/stringUtils";

function MetadataRow({ label, value }: { label: string; value: string }) {
  return (
    <tr>
      <th className="py-2 pr-4 w-40">{label}</th>
      <td className="py-2">{value}</td>
    </tr>
  );
}

// Type for device metrics returned from GraphQL
type DeviceData = {
  hostname: string;
  uptime?: number;
  sysUptime?: number;
  cpuUtilization: number;
  memoryUtilization: number;
  timestamp: string; // ISO string from API
  sysName?: string;
  sysDescription?: string;
  sysObjectid?: string;
};

type DeviceDetailsProps = {
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
    { timestamp: string; value: number }[]
  >([]);
  const [cpuUsageData, setCpuUsageData] = useState<
    { timestamp: string; value: number }[]
  >([]);
  const [memoryUsageData, setMemoryUsageData] = useState<
    { timestamp: string; value: number }[]
  >([]);
  const [deviceMetrics, setDeviceMetrics] = useState<DeviceData | null>(null);

  const [selectedRange, setSelectedRange] = useState<number>(1);
  const [errorMsg, setErrorMsg] = useState("");
  const [customRange, setCustomRange] = useState<{
    start: string;
    end: string;
  }>({ start: "", end: "" });
  const [open, setOpen] = useState<boolean>(false);
  const topologyChartMemo = useMemo(
    () => (
      <TopologyChart
        devices={[device]}
        loading={false}
        error={null}
        zoomView={false}
        clickToUse={false}
      />
    ),
    [device] // only re-render if device changes
  );
  const metadataTableMemo = useMemo(
    () => (
      <div className="max-w-full h-[400px] min-w-[300px] w-[50vw] p-5 bg-content-bg items-center justify-center border border-border-subtle rounded-lg lg:w-[50vw] xl:w-[35vw]">
        <table
          className={`table-auto w-fit m-top-0 text-left ${styles.tableCustom}`}
        >
          <tbody className="text-xs md:text-sm">
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
              value={
                typeof device.sysUptime === "number" && device.sysUptime > 0
                  ? "Up"
                  : "Down"
              }
            />
            <MetadataRow
              label="Uptime"
              value={
                formatUptime(device.sysUptime ?? deviceMetrics?.uptime ?? 0) ??
                "N/A"
              }
            />
            <MetadataRow label="System ID" value={device.sysObjectid ?? "-"} />
            <MetadataRow
              label="Time Last Polled"
              value={
                deviceMetrics ? formatUnixTimestamp(device.lastPolled) : "-"
              }
            />
          </tbody>
        </table>
      </div>
    ),
    [device, deviceMetrics] // only re-render if device or deviceMetrics change
  );

  const query = `
    query {
      deviceMetrics(hostname: "${device.hostname}") {
        edges {
          node {
            hostname
            uptime
            cpuUtilization
            memoryUtilization
            timestamp
          }
        }
      }
    }
    `;

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://localhost:7000/switchmap/api/graphql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        });
        const json = await res.json();

        const hostMetrics: DeviceData[] = json.data.deviceMetrics.edges.map(
          ({ node }: { node: DeviceData }) => node
        );

        if (hostMetrics.length === 0) return;

        hostMetrics.sort(
          (a, b) =>
            new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        );

        setDeviceMetrics(hostMetrics[hostMetrics.length - 1]);

        setUptimeData(
          hostMetrics.map((m) => ({
            timestamp: new Date(m.timestamp).toISOString(),
            value: (m.sysUptime ?? m.uptime ?? 0) / 1000000,
          }))
        );

        setCpuUsageData(
          hostMetrics.map((m) => ({
            timestamp: new Date(m.timestamp).toISOString(),
            value: m.cpuUtilization,
          }))
        );

        setMemoryUsageData(
          hostMetrics.map((m) => ({
            timestamp: new Date(m.timestamp).toISOString(),
            value: m.memoryUtilization,
          }))
        );
      } catch (error) {
        console.error("Error fetching device metrics:", error);
      }
    }

    fetchData();
  }, [device.hostname]);

  const filterByRange = (data: { timestamp: string; value: number }[]) => {
    const now = new Date();
    let startDate: Date;

    if (selectedRange === 0 && customRange.start && customRange.end) {
      startDate = new Date(customRange.start);
      const endDate = new Date(customRange.end);
      return data.filter(
        (d) =>
          new Date(d.timestamp) >= startDate && new Date(d.timestamp) <= endDate
      );
    } else {
      startDate = new Date();
      startDate.setDate(now.getDate() - selectedRange);
      return data.filter((d) => new Date(d.timestamp) >= startDate);
    }
  };

  return (
    <div className="p-8 w-[85vw] flex flex-col gap-4 h-full ">
      {/* Centralized error alert */}
      {errorMsg && (
        <div className="fixed inset-0 flex mt-2 items-start justify-center z-50 pointer-events-none">
          <div className="bg-gray-300 text-gray-900 px-6 py-3 rounded shadow-lg animate-fade-in pointer-events-auto">
            {errorMsg}
          </div>
        </div>
      )}
      <h2 className="text-xl font-semibold mb-2">Device Overview</h2>
      <div
        className={`flex flex-col md:flex-row md:self-center gap-2 ${styles.deviceChartWrapper}`}
      >
        {topologyChartMemo}
        {metadataTableMemo}
      </div>
      {/* Time Range Dropdown */}
      <div className="mt-8 md:mt-2 flex flex-col md:flex-row gap-4 text-left justify-start xl:items-center">
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
          <div className="flex flex-col sm:flex-row gap-2 items-start">
            <input
              type="date"
              className="border p-2 rounded"
              value={customRange.start}
              onChange={(e) => {
                const start = new Date(e.target.value);
                const end = customRange.end ? new Date(customRange.end) : null;
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
            <span className="flex items-center justify-center h-full px-2 my-auto">
              to
            </span>
            <input
              type="date"
              className="border p-2 rounded"
              value={customRange.end}
              onChange={(e) => {
                const start = customRange.start
                  ? new Date(customRange.start)
                  : null;
                const end = new Date(e.target.value);

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
          </div>
        )}
      </div>

      <div className="p-4 w-full min-w-[350px] flex flex-col xl:flex-row gap-4">
        <HistoricalChart
          title="Uptime (%)"
          data={filterByRange(uptimeData)}
          color="#00b894"
          unit="%"
        />
        <HistoricalChart
          title="CPU Usage (%)"
          data={filterByRange(cpuUsageData)}
          color="#0984e3"
          unit="%"
        />
        <HistoricalChart
          title="Memory Usage (%)"
          data={filterByRange(memoryUsageData)}
          color="#e17055"
          unit="%"
        />
      </div>
    </div>
  );
}
