"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Device = {
  idxDevice: string;
  id: string;
  sysName: string | null;
  hostname: string | null;
  sysObjectid: string | null;
  sysUptime: number;
  l1interfaces: {
    edges: { node: { ifoperstatus: number } }[];
  };
};

const formatUptime = (hundredths: number) => {
  const seconds = Math.floor(hundredths / 100);
  const days = Math.floor(seconds / 86400);
  const hrs = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${days}d ${hrs}h ${mins}m ${secs}s`;
};
const mapOidToType = (oid: string | null) => {
  if (!oid) return "-";
  // TODO: Add device type such as router, switch, etc.
  if (oid.startsWith(".1.3.6.1.4.1.9.1.")) return "Cisco";
  if (oid.startsWith(".1.3.6.1.4.1.2636.1.")) return "Juniper";
  // Add more mappings as needed
  return "Unknown";
};

export default function DevicesOverview() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDevices = async () => {
      const res = await fetch("http://localhost:7000/switchmap/api/graphql", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: `
            {
              devices {
                edges {
                  node {
                    id
                    idxDevice
                    sysName
                    hostname
                    sysObjectid
                    sysUptime
                    l1interfaces {
                      edges {
                        node {
                          ifoperstatus
                        }
                      }
                    }
                  }
                }
              }
            }
          `,
        }),
      });
      const json = await res.json();
      const rawDevices = json.data.devices.edges.map((edge: any) => edge.node);
      setDevices(rawDevices);
      setLoading(false);
    };

    fetchDevices();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Devices Overview</h2>
      <table border={1} cellPadding={8} cellSpacing={0}>
        <thead>
          <tr>
            <th>Device Name</th>
            <th>Hostname</th>
            <th>Type (OID)</th>
            <th>Active Ports</th>
            <th>Uptime</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((device) => {
            const interfaces = device.l1interfaces.edges.map((e) => e.node);
            const total = interfaces.length;
            const active = interfaces.filter(
              (p) => p.ifoperstatus === 1
            ).length;

            return (
              <tr key={device.id}>
                <td>
                  <Link
                    href={`/devices/${encodeURIComponent(
                      device.idxDevice ?? device.id
                    )}?sysName=${encodeURIComponent(
                      device.sysName ?? device.hostname ?? ""
                    )}#devices-overview`}
                  >
                    {device.sysName || "-"}
                  </Link>
                </td>
                <td>{device.hostname || "-"}</td>
                <td>{mapOidToType(device.sysObjectid)}</td>
                <td>{`${active}/${total}`}</td>
                <td>{formatUptime(device.sysUptime)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
