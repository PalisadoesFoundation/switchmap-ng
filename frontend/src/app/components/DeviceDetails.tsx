import React from "react";
import HistoricalChart from "./HistoricalChart";
import { TopologyChart } from "./TopologyChart";
import { DeviceNode } from "../types/graphql/GetZoneDevices";
import styles from "./DeviceDetails.module.css";
import { formatUptime } from "../utils/time";
import { formatUnixTimestamp } from "../utils/timeStamp";
import { truncateLines } from "../utils/stringUtils";

const uptimeData = [
  { timestamp: "2025-07-29 00:00", value: 99.95 },
  { timestamp: "2025-07-29 01:00", value: 99.97 },
  { timestamp: "2025-07-29 02:00", value: 99.92 },
];
function MetadataRow({ label, value }: { label: string; value: string }) {
  return (
    <tr>
      <th className="py-2 pr-4 w-40">{label}</th>
      <td className="py-2 border-b">{value}</td>
    </tr>
  );
}

export function DeviceDetails({ device }: { device: DeviceNode }) {
  return (
    <div className="p-4 w-full flex flex-col gap-4 h-full">
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
        <div className="max-w-[60vw] items-center justify-center">
          <table className="table-auto w-fit! m-top-0 text-left border-collapse">
            <tbody className="text-xs md:text-base">
              <MetadataRow label="Device Name" value={device.sysName} />
              <MetadataRow
                label="Description"
                value={truncateLines(device.sysDescription)}
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
                value={formatUptime(device.sysUptime) ?? "N/A"}
              />
              <MetadataRow label="System ID" value={device.sysObjectid} />
              <MetadataRow
                label="Time Last Polled"
                value={formatUnixTimestamp(device.lastPolled)}
              />
            </tbody>
          </table>
        </div>
      </div>
      <div className="p-4 w-full flex flex-row">
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
