"use client";

import DevicesOverview from "@/components/DevicesOverview";
import ZoneDropdown from "@/components/ZoneDropdown";
import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import TopologyChart from "@/components/TopologyChart";
import { DeviceNode, GetZoneDevicesData } from "@/types/graphql/GetZoneDevices";

export default function Home() {
  const [zoneId, setZoneId] = useState<string>("");
  const [zoneSelected, setZoneSelected] = useState<boolean>(false);

  // Add these states for device data
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
  useEffect(() => {
    if (!zoneId) {
      setDevices([]);
      setLoading(false);
      setError("Waiting for zone selection to load devices.");
      return;
    }

    const fetchDevices = async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await fetch(
          process.env.NEXT_PUBLIC_API_URL ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              query: `
                query GetZoneDevices($id: ID!) {
                  zone(id: $id) {
                    devices {
                      edges {
                        node {
                          idxDevice
                          sysObjectid
                          sysUptime
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
              `,
              variables: { id: zoneId },
            }),
          }
        );

        if (!res.ok)
          throw new Error(`Network response was not ok: ${res.statusText}`);

        const json: GetZoneDevicesData = await res.json();
        if (json.errors)
          throw new Error(json.errors.map((e: any) => e.message).join(", "));

        const rawDevices = json.data.zone.devices.edges.map(
          (edge) => edge.node
        );
        setDevices(rawDevices);
      } catch (err: unknown) {
        let errorMessage =
          "Failed to load devices. Please check your network or try again.";

        if (err instanceof Error) {
          console.error("Error fetching devices:", err.message);
          errorMessage = err.message;
        } else {
          console.error("Unknown error", err);
        }

        setDevices([]);
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, [zoneId]);

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-y-auto overflow-x-hidden">
        <div className="sticky top-0 z-10 bg-transparent lg:bg-blend-soft-light flex justify-end p-4">
          <ZoneDropdown selectedZoneId={zoneId} onChange={setZoneId} />
        </div>

        <div id="network-topology" className="h-screen mb-8 p-8">
          {zoneSelected && (
            <TopologyChart devices={devices} loading={loading} error={error} />
          )}
        </div>

        <div id="devices-overview" className="h-screen p-8">
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
