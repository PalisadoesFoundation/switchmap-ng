/**
 * Utility functions for device management, including date parsing and filtering.
 * 
 * @remarks
 * This module provides functions to parse date strings and filter devices based on their last polled time.
 * It includes a type definition for device nodes used in the application.
 * 
 * @see {@link DeviceNode} for the device node structure.
 * @see {@link parseDateOnlyLocal} for parsing date strings.
 * @see {@link filterDevicesByTimeRange} for filtering devices by time range.
 */


export type DeviceNode = {
  hostname: string;
  lastPolledMs?: number | null;
};

/** Parses a YYYY-MM-DD string to a local Date */
export function parseDateOnlyLocal(yyyyMmDd: string): Date {
  const [y, m, d] = yyyyMmDd.split("-").map(Number);
  return new Date(y, (m ?? 1) - 1, d ?? 1);
}

/** Filters devices by time range */
export function filterDevicesByTimeRange(
  devices: DeviceNode[],
  timeRange: string,
  start?: string,
  end?: string
): DeviceNode[] {
  const now = new Date();

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
