import React from "react";
import HistoricalChart from "./HistoricalChart";
import { TopologyChart } from "./TopologyChart";
import { DeviceNode } from "../types/graphql/GetZoneDevices";
import styles from "./DeviceDetails.module.css";

const uptimeData = [
  { timestamp: "2025-07-29 00:00", value: 99.98 },
  { timestamp: "2025-07-29 01:00", value: 99.96 },
  { timestamp: "2025-07-29 02:00", value: 99.92 },
  { timestamp: "2025-07-29 03:00", value: 99.95 },
  { timestamp: "2025-07-29 04:00", value: 99.9 },
  { timestamp: "2025-07-29 05:00", value: 99.94 },
];

const cpuUsageData = [
  { timestamp: "2025-07-29 00:00", value: 15.2 },
  { timestamp: "2025-07-29 01:00", value: 22.5 },
  { timestamp: "2025-07-29 02:00", value: 18.7 },
  { timestamp: "2025-07-29 03:00", value: 25.3 },
  { timestamp: "2025-07-29 04:00", value: 30.1 },
  { timestamp: "2025-07-29 05:00", value: 19.8 },
];

const memoryUsageData = [
  { timestamp: "2025-07-29 00:00", value: 45.0 },
  { timestamp: "2025-07-29 01:00", value: 47.8 },
  { timestamp: "2025-07-29 02:00", value: 49.5 },
  { timestamp: "2025-07-29 03:00", value: 52.3 },
  { timestamp: "2025-07-29 04:00", value: 55.0 },
  { timestamp: "2025-07-29 05:00", value: 50.1 },
];

export function DeviceDetails({ device }: { device: DeviceNode }) {
  return (
    <div className="p-4 w-full flex flex-col gap-4 h-full">
      <h2 className="text-xl font-semibold mb-2">Device Overview</h2>
      <div
        className={`w-[50vw] h-[50vh] flex flex-row gap-2 ${styles.deviceChartWrapper}`}
      >
        <TopologyChart
          devices={[device]}
          loading={false}
          error={null}
          zoomView={false}
          clickToUse={false}
        />
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
