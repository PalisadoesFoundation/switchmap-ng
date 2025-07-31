import React from "react";
import HistoricalChart from "./HistoricalChart";

const uptimeData = [
  { timestamp: "2025-07-29 00:00", value: 99.95 },
  { timestamp: "2025-07-29 01:00", value: 99.97 },
  { timestamp: "2025-07-29 02:00", value: 99.92 },
];

export function DeviceDetails() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Device Uptime (Past 48h)</h1>
      <HistoricalChart
        title="Uptime (%)"
        data={uptimeData}
        color="#00b894"
        unit="%"
      />
    </div>
  );
}
