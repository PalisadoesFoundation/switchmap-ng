/// <reference types="vitest" />
import { describe, it, expect } from "vitest";
import {
  DeviceNode,
  filterDevicesByTimeRange,
  parseDateOnlyLocal,
} from "./deviceUtils";

describe("parseDateOnlyLocal", () => {
  it("parses YYYY-MM-DD correctly", () => {
    const date = parseDateOnlyLocal("2025-10-08");
    expect(date.getFullYear()).toBe(2025);
    expect(date.getMonth()).toBe(9);
    expect(date.getDate()).toBe(8);
  });
});

describe("filterDevicesByTimeRange", () => {
  const now = Date.now();
  const oneDayMs = 24 * 60 * 60 * 1000;

  const devices: DeviceNode[] = [
    { hostname: "dev1", lastPolledMs: now },
    { hostname: "dev2", lastPolledMs: now - oneDayMs * 2 },
    { hostname: "dev3", lastPolledMs: undefined },
    { hostname: "dev4", lastPolledMs: NaN },
  ];

  it("filters devices for custom range with valid dates", () => {
    const start = new Date(now - oneDayMs).toISOString().split("T")[0];
    const end = new Date(now + oneDayMs).toISOString().split("T")[0];
    const result = filterDevicesByTimeRange(devices, "custom", start, end);
    expect(result.map((d) => d.hostname)).toContain("dev1");
    expect(result.map((d) => d.hostname)).not.toContain("dev3");
    expect(result.map((d) => d.hostname)).not.toContain("dev4");
  });

  it("returns all devices if custom range but start/end missing", () => {
    const result = filterDevicesByTimeRange(devices, "custom");
    expect(result).toEqual(devices);
  });

  it("filters devices for 1d, 1w, 1m, 6m ranges", () => {
    ["1d", "1w", "1m", "6m"].forEach((range) => {
      const result = filterDevicesByTimeRange(devices, range);
      expect(result).toContainEqual(devices[0]);
    });
  });

  it("returns all devices if invalid range", () => {
    const result = filterDevicesByTimeRange(devices, "invalid");
    expect(result).toEqual(devices);
  });

  it("excludes devices with invalid lastPolledMs", () => {
    const start = new Date(now - oneDayMs).toISOString().split("T")[0];
    const end = new Date(now + oneDayMs).toISOString().split("T")[0];
    const result = filterDevicesByTimeRange(devices, "custom", start, end);
    result.forEach((d) => expect(typeof d.lastPolledMs).toBe("number"));
  });
});
