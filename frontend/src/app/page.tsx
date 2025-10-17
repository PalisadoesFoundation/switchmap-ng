"use client";

import {
  useEffect,
  useState,
  useCallback,
  useMemo,
  lazy,
  Suspense,
} from "react";
import { Sidebar } from "@/app/components/Sidebar";
import { ZoneDropdown } from "@/app/components/ZoneDropdown";
import {
  DeviceNode,
  GetZoneDevicesData,
} from "@/app/types/graphql/GetZoneDevices";

// Lazy load heavy components
const TopologyChart = lazy(() =>
  import("@/app/components/TopologyChart").then((mod) => ({
    default: mod.TopologyChart,
  }))
);
const DevicesOverview = lazy(() =>
  import("@/app/components/DevicesOverview").then((mod) => ({
    default: mod.DevicesOverview,
  }))
);

// Cache for device data with timestamp
interface CacheEntry {
  data: DeviceNode[];
  timestamp: number;
}

const deviceCache = new Map<string, CacheEntry>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

/**
 * Home page component displaying network topology and devices overview.
 *
 * @remarks
 * This component fetches and displays devices based on the selected zone.
 * It includes a sidebar, a zone selection dropdown, a topology chart, and
 * a devices overview section. The component uses caching to minimize
 * unnecessary API calls and improve performance.
 *
 * @returns The main home page component.
 *
 * @see {@link Sidebar} for the navigation sidebar.
 * @see {@link ZoneDropdown} for selecting network zones.
 * @see {@link TopologyChart} for visualizing network topology.
 * @see {@link DevicesOverview} for listing devices in a tabular format.
 */
export default function Home() {
  const [zoneId, setZoneId] = useState<string>("");
  const [zoneSelected, setZoneSelected] = useState<boolean>(false);
  const [devices, setDevices] = useState<DeviceNode[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Track ongoing requests to prevent duplicates
  const [ongoingRequest, setOngoingRequest] = useState<AbortController | null>(
    null
  );

  // Memoize GraphQL queries
  const GET_ZONE_DEVICES = useMemo(
    () => `
    query GetZoneDevices($id: ID!) {
      zone(id: $id) {
        devices {
          edges {
            node {
              idxDevice
              sysObjectid
              sysUptime
              sysDescription
              sysName
              hostname
              l1interfaces {
                edges {
                  node {
                    ifoperstatus
                    cdpcachedeviceid
                    cdpcachedeviceport
                    lldpremportdesc
                    lldpremsysname
                    lldpremsysdesc
                    lldpremsyscapenabled 
                  }
                }
              }
            }
          }
        }
      }
    }
  `,
    []
  );

  const GET_ALL_ZONES_DEVICES = useMemo(
    () => `
    query GetAllZonesDevices {
      events(last: 1) {
        edges {
          node {
            zones {
              edges {
                node {
                  devices {
                    edges {
                      node {
                        idxDevice
                        sysObjectid
                        sysUptime
                        sysDescription
                        sysName
                        hostname
                        l1interfaces {
                          edges {
                            node {
                              ifoperstatus
                              cdpcachedeviceid
                              cdpcachedeviceport
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  `,
    []
  );

  // Initialize from localStorage
  useEffect(() => {
    const storedZoneId = localStorage.getItem("zoneId") || "";
    setZoneId(storedZoneId);

    const hash = window.location.hash;
    if (hash) {
      setTimeout(() => {
        const el = document.querySelector(hash);
        if (el) el.scrollIntoView({ behavior: "smooth" });
      }, 100);
    }
  }, []);

  // Persist zone selection
  useEffect(() => {
    if (zoneId) {
      localStorage.setItem("zoneId", zoneId);
      setZoneSelected(!!zoneId);
    }
  }, [zoneId]);

  // Check cache validity
  const getCachedDevices = useCallback(
    (zoneKey: string): DeviceNode[] | null => {
      const cached = deviceCache.get(zoneKey);
      if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        return cached.data;
      }
      return null;
    },
    []
  );

  // Deduplicate devices by hostname
  const deduplicateDevices = useCallback((devices: any[]): DeviceNode[] => {
    const seen = new Map<string, any>();
    devices.forEach((dev: any) => {
      if (dev.hostname) seen.set(dev.hostname, dev);
    });
    return Array.from(seen.values()) as DeviceNode[];
  }, []);

  // Optimized fetch with caching and deduplication
  const fetchDevices = useCallback(
    async (currentZoneId: string) => {
      if (!currentZoneId) {
        setDevices([]);
        setLoading(false);
        setError("Waiting for zone selection to load devices.");
        return;
      }

      // Cancel any ongoing request
      if (ongoingRequest) {
        ongoingRequest.abort();
      }

      // Check cache first
      const cached = getCachedDevices(currentZoneId);
      if (cached) {
        setDevices(cached);
        setLoading(false);
        setError(null);
        return;
      }

      const abortController = new AbortController();
      setOngoingRequest(abortController);

      try {
        setLoading(true);
        setError(null);

        const query =
          currentZoneId === "all" ? GET_ALL_ZONES_DEVICES : GET_ZONE_DEVICES;
        const variables = currentZoneId === "all" ? {} : { id: currentZoneId };

        const res = await fetch(
          process.env.NEXT_PUBLIC_API_URL ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, variables }),
            signal: abortController.signal,
          }
        );

        if (!res.ok) throw new Error(`Network error: ${res.statusText}`);
        const json = await res.json();

        if (json.errors)
          throw new Error(json.errors.map((e: any) => e.message).join(", "));

        let rawDevices: DeviceNode[] = [];

        if (currentZoneId === "all") {
          const allDevices =
            json?.data?.events?.edges?.[0]?.node?.zones?.edges?.flatMap(
              (z: any) => z?.node?.devices?.edges?.map((d: any) => d.node) ?? []
            ) ?? [];
          rawDevices = deduplicateDevices(allDevices);
        } else {
          const zoneDevices =
            json?.data?.zone?.devices?.edges?.map((d: any) => d.node) ?? [];
          rawDevices = deduplicateDevices(zoneDevices);
        }

        // Cache the results
        deviceCache.set(currentZoneId, {
          data: rawDevices,
          timestamp: Date.now(),
        });

        setDevices(rawDevices);
      } catch (err: any) {
        if (err.name === "AbortError") {
          return;
        }

        const message =
          err instanceof Error
            ? err.message
            : typeof err === "string"
            ? err
            : "Failed to load devices. Please check your network or try again.";
        console.error("Error fetching devices:", message);
        setDevices([]);
        setError(message);
      } finally {
        setLoading(false);
        setOngoingRequest(null);
      }
    },
    [
      GET_ZONE_DEVICES,
      GET_ALL_ZONES_DEVICES,
      getCachedDevices,
      deduplicateDevices,
      ongoingRequest,
    ]
  );

  // Debounce device fetching
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchDevices(zoneId);
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [zoneId]);

  // Loading fallback component
  const LoadingFallback = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-500">Loading component...</div>
    </div>
  );

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 lg:ml-60">
        <div className="sticky top-0 z-10 bg-bg lg:bg-blend-soft-light flex justify-end p-4">
          <ZoneDropdown selectedZoneId={zoneId} onChange={setZoneId} />
        </div>

        <div id="network-topology" className="h-screen mb-8 p-8">
          {zoneSelected && (
            <Suspense fallback={<LoadingFallback />}>
              <TopologyChart
                devices={devices}
                loading={loading}
                error={error}
              />
            </Suspense>
          )}
        </div>

        <div id="devices-overview" className="h-fit p-8">
          {zoneSelected && (
            <Suspense fallback={<LoadingFallback />}>
              <DevicesOverview
                devices={devices}
                loading={loading}
                error={error}
              />
            </Suspense>
          )}
        </div>
      </main>
    </div>
  );
}

export const _testUtils = {
  clearDeviceCache: () => deviceCache.clear(),
};
