import React, { useEffect, useState } from "react";
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

  const query = `
    query {
      allDeviceMetrics {
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

        const devices: DeviceData[] = json.data.allDeviceMetrics.edges.map(
          ({ node }: { node: DeviceData }) => node
        );

        // all records for this device
        const hostMetrics = devices.filter(
          (d) => d.hostname === device.hostname
        );
        if (hostMetrics.length === 0) return;

        // sort by timestamp (oldest → newest)
        hostMetrics.sort(
          (a, b) =>
            new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        );

        setDeviceMetrics(hostMetrics[hostMetrics.length - 1]); // latest snapshot

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
        console.error("Error fetching devices data:", error);
      }
    }

    fetchData();
  }, [device.hostname]);

  return (
    <div className="p-4 w-[85vw] flex flex-col gap-4 h-full">
      <h2 className="text-xl font-semibold mb-2">Device Overview</h2>
      <div
        className={`h-[45vh] flex flex-row gap-2 ${styles.deviceChartWrapper}`}
      >
        <TopologyChart
          devices={[device]}
          loading={false}
          error={null}
          zoomView={false}
          clickToUse={false}
        />
        <div className="max-w-full p-5 mr-5 bg-content-bg items-center justify-center border border-border-subtle rounded-lg">
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
                  formatUptime(
                    device.sysUptime ?? deviceMetrics?.uptime ?? 0
                  ) ?? "N/A"
                }
              />
              <MetadataRow
                label="System ID"
                value={device.sysObjectid ?? "-"}
              />
              <MetadataRow
                label="Time Last Polled"
                value={
                  deviceMetrics
                    ? formatUnixTimestamp(deviceMetrics.timestamp)
                    : "-"
                }
              />
            </tbody>
          </table>
        </div>
      </div>
      <div className="p-4 w-full flex flex-row gap-4">
        <HistoricalChart
          title="Uptime (%)"
          data={uptimeData}
          color="#00b894"
          unit="%"
        />
        <HistoricalChart
          title="CPU Usage (%)"
          data={cpuUsageData}
          color="#0984e3"
          unit="%"
        />
        <HistoricalChart
          title="Memory Usage (%)"
          data={memoryUsageData}
          color="#e17055"
          unit="%"
        />
      </div>
    </div>
  );
}
