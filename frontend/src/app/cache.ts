// cache.ts
import { DeviceNode } from "@/app/types/graphql/GetZoneDevices";

export interface CacheEntry {
  data: DeviceNode[];
  timestamp: number;
}

// Central cache for devices
export const deviceCache = new Map<string, CacheEntry>();

// Utility to clear cache (for testing)
export const __resetDeviceCache = () => {
  deviceCache.clear();
};
