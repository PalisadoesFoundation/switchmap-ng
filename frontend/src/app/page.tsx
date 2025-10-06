"use client";

import { DevicesOverview } from "@/app/components/DevicesOverview";
import { ZoneDropdown } from "@/app/components/ZoneDropdown";
import { useEffect, useState } from "react";
import { Sidebar } from "@/app/components/Sidebar";
import { TopologyChart } from "@/app/components/TopologyChart";
import {
  DeviceNode,
  GetZoneDevicesData,
} from "@/app/types/graphql/GetZoneDevices";

/**
 * Main entry point for the application.
 *
 * This component renders the sidebar and main content area,
 * including the network topology and devices overview sections.
 * It also manages the selected zone state and persists it in localStorage.
 *
 * @remarks
 * This component is the main page of the application.
 * It initializes the zone ID from localStorage and updates it
 * whenever the user selects a different zone.
 * It also handles scrolling to elements based on the URL hash.
 * It uses the `Sidebar` component for navigation and the `ZoneDropdown`
 * component for selecting zones.
 *
 * @returns The rendered component.
 *
 * @see {@link Sidebar} for the sidebar component.
 * @see {@link ZoneDropdown} for the zone selection dropdown.
 * @see {@link DevicesOverview} for displaying devices in the selected zone.
 */
export default function Home() {
  const [zoneId, setZoneId] = useState<string>("");
  const [zoneSelected, setZoneSelected] = useState<boolean>(false);
  const [devices, setDevices] = useState<DeviceNode[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setZoneId(localStorage.getItem("zoneId") || "");
    const hash = window.location.hash;
    if (hash) {
      const el = document.querySelector(hash);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  useEffect(() => {
    if (zoneId) {
      localStorage.setItem("zoneId", zoneId);
      setZoneSelected(!!zoneId);
    }
  }, [zoneId]);

  // New: fetch devices when zoneId changes
  const GET_ZONE_DEVICES = `
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
`;

  useEffect(() => {
    if (!zoneId) {
      setDevices([]);
      setLoading(false);
      setError("Waiting for zone selection to load devices.");
      return;
    }

    const fetchDevices = async (retryCount = 0) => {
      try {
        setLoading(true);
        setError(null);

        const query =
          zoneId === "all"
            ? `
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
        `
            : GET_ZONE_DEVICES;

        const variables = zoneId === "all" ? {} : { id: zoneId };

        const res = await fetch(
          process.env.NEXT_PUBLIC_API_URL ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, variables }),
          }
        );

        if (!res.ok) throw new Error(`Network error: ${res.statusText}`);
        const json = await res.json();

        if (json.errors)
          throw new Error(json.errors.map((e: any) => e.message).join(", "));

        let rawDevices: DeviceNode[] = [];

        if (zoneId === "all") {
          const devices =
            json?.data?.events?.edges?.[0]?.node?.zones?.edges?.flatMap(
              (z: any) => z?.node?.devices?.edges?.map((d: any) => d.node) ?? []
            ) ?? [];

          // Deduplicate by hostname
          const seen = new Map<string, any>();
          devices.forEach((dev: any) => {
            if (dev.hostname) seen.set(dev.hostname, dev);
          });
          rawDevices = Array.from(seen.values()) as DeviceNode[];
        } else {
          const devices =
            json?.data?.zone?.devices?.edges?.map((d: any) => d.node) ?? [];

          // Deduplicate by hostname
          const seen = new Map<string, any>();
          devices.forEach((dev: any) => {
            if (dev.hostname) seen.set(dev.hostname, dev);
          });
          rawDevices = Array.from(seen.values()) as DeviceNode[];
        }
        setDevices(rawDevices);
      } catch (err: any) {
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
      }
    };

    fetchDevices();
  }, [zoneId]);

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1">
        <div className="sticky top-0 z-10 bg-bg lg:bg-blend-soft-light flex justify-end p-4">
          <ZoneDropdown selectedZoneId={zoneId} onChange={setZoneId} />
        </div>

        <div id="network-topology" className="h-screen mb-8 p-8">
          {zoneSelected && (
            <TopologyChart devices={devices} loading={loading} error={error} />
          )}
        </div>

        <div id="devices-overview" className="h-fit p-8">
          {zoneSelected && (
            <DevicesOverview
              devices={devices}
              loading={loading}
              error={error}
            />
          )}
        </div>
      </main>
    </div>
  );
}
