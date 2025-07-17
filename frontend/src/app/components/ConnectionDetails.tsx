"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  InterfaceEdge,
  InterfaceNode,
  Mac,
  MacPorts,
  MacsEdge,
} from "../../../types/graphql/GetDeviceInterfaces";
import { DeviceNode } from "../../../types/graphql/GetZoneDevices";

type DeviceResponse = {
  device: DeviceNode | null;
};

// GraphQL query to fetch device interface details
const QUERY = `
  query Device($id: ID!) {
    device(id: $id) {
      l1interfaces {
        edges {
          node {
            idxL1interface
            idxDevice
            ifname
            nativevlan
            ifoperstatus
            tsIdle
            ifspeed
            duplex
            ifalias
            trunk
            cdpcachedeviceid
            cdpcachedeviceport
            cdpcacheplatform
            lldpremportdesc
            lldpremsysname
            lldpremsysdesc
            lldpremsyscapenabled
            macports{
              edges{
                node{
                  macs{
                    mac
                    oui{
                      organization
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
`;

//Testing for auto docs

function ConnectionDetails({ deviceId }: { deviceId?: string }) {
  const params = useParams();
  // Determine device ID from props or URL params
  const id =
    deviceId ??
    (typeof params?.id === "string"
      ? decodeURIComponent(params.id)
      : Array.isArray(params?.id) && params.id.length > 0
      ? decodeURIComponent(params.id[0])
      : undefined);

  const [data, setData] = useState<DeviceResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Helper functions for MAC address processing
  const extractMacAddresses = (macports?: MacPorts): string => {
    if (!Array.isArray(macports?.edges) || macports.edges.length === 0)
      return "";

    return macports.edges
      .flatMap((edge) => {
        const macs = edge?.node?.macs;
        const macList = Array.isArray(macs) ? macs : macs ? [macs] : [];
        return macList.map((macObj) => macObj?.mac).filter(Boolean);
      })
      .join(", ");
  };

  const extractManufacturers = (macports?: MacPorts): string => {
    if (!Array.isArray(macports?.edges) || macports.edges.length === 0)
      return "";

    return macports.edges
      .flatMap((edge) => {
        const macs = edge?.node?.macs;
        const macList = Array.isArray(macs) ? macs : macs ? [macs] : [];
        return macList
          .map((macObj) => macObj?.oui?.organization || "")
          .filter(Boolean);
      })
      .join(", ");
  };

  // Fetch device data when ID changes
  useEffect(() => {
    if (!id) return;

    setLoading(true);
    setError(null);
    const globalId = id && typeof id === "string" ? btoa(`Device:${id}`) : id;

    fetch("http://localhost:7000/switchmap/api/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: QUERY,
        variables: { id: globalId },
      }),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Network error: ${res.status}`);
        return res.json();
      })
      .then((deviceJson) => {
        if (deviceJson.errors) throw new Error(deviceJson.errors[0].message);
        setDeviceData(deviceJson.data);

        const idxL1interfaces = deviceJson.data.device.l1interfaces.edges.map(
          (edge: any) => edge.node.idxL1interface
        );
        console.log("Fetching MAC/IP for interfaces:", idxL1interfaces);

        if (idxL1interfaces.length === 0) {
          setMacportsData({ macports: { edges: [] } });
          return null;
        }
        console.log("Sending MACPORTS query with ids:", idxL1interfaces);
        const query = MACPORTS_QUERY(idxL1interfaces.map(Number));

        console.log("MACPORTS inline query:\n", query);

        return fetch("http://localhost:7000/switchmap/api/graphql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        });
      })
      .then((res) => {
        if (!res) return; // No macports query if no interfaces
        if (!res.ok) throw new Error(`Network error: ${res.status}`);
        return res.json();
      })
      .then((macportsJson) => {
        if (!macportsJson) return;
        console.log("MAC/IP fetched data:", macportsJson);
        if (macportsJson.errors)
          throw new Error(macportsJson.errors[0].message);
        setMacportsData(macportsJson.data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  // Handle loading, error, and missing data states
  if (!id) return <p>Error: No device ID provided.</p>;
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!data) return null;
  if (!data.device || !data.device.l1interfaces)
    return <p>No interface data available.</p>;

  // Extract interface list
  const interfaces = data.device.l1interfaces.edges.map(
    ({ node }: InterfaceEdge) => node
  );

  type MacportNode = {
    idxL1interface: number;
    macs?: {
      mac: string;
      oui?: {
        organization?: string;
      };
    };
  };

  const macportsNodes: MacportNode[] = macportsData.macports.edges.map(
    ({ node }: { node: MacportNode }) => node
  );

  const macportsNodesByIdx = new Map(
    macportsNodes
      .filter((node) => node && node.idxL1interface !== undefined)
      .map((node) => [node.idxL1interface, node])
  );

  return (
    <div className="w-[87%] h-[80vh]">
      <h2 className="mb-4">Connection Details</h2>
      <div className="w-full h-full overflow-auto border border-border rounded-lg shadow-sm">
        <table
          className="w-full h-full border border-border rounded-lg shadow-sm"
          style={{ marginTop: "0rem" }}
        >
          <thead>
            <tr className="sticky top-0 bg-bg z-10">
              {[
                "Port",
                "VLAN",
                "State",
                "Days Inactive",
                "Speed",
                "Duplex",
                "Port Label",
                "Trunk",
                "CDP",
                "LLDP",
                "Mac Address",
                "Manufacturer",
                "IP Address",
                "DNS Name",
              ].map((title) => (
                <th key={title}>{title}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {interfaces.map((iface: InterfaceNode) => (
              <tr
                key={iface.idxDevice + iface.ifname}
                className={`
                  ${
                    iface.ifoperstatus === 1
                      ? "bg-[#0072B2]/10 dark:bg-[#56B4E9]/10"
                      : iface.ifoperstatus === 2
                      ? "bg-[#E69F00]/10 dark:bg-[#F0E442]/10"
                      : "bg-gray-100/10 dark:bg-gray-700/10"
                  }
                  transition-colors duration-300
  `}
              >
                <td>{iface.ifname || "N/A"}</td>
                <td>{iface.nativevlan ?? "N/A"}</td>
                <td>
                  {iface.ifoperstatus == 1
                    ? "Active"
                    : iface.ifoperstatus == 2
                    ? "Disabled"
                    : "N/A"}
                </td>
                <td>{iface.tsIdle ?? "N/A"}</td>
                <td>{iface.ifspeed ?? "N/A"}</td>
                <td>{iface.duplex ?? "N/A"}</td>
                <td>{iface.ifalias || "N/A"}</td>
                <td>{iface.trunk ? "Trunk" : "-"}</td>
                <td>{iface.cdpcachedeviceid || "-"}</td>
                <td>{iface.lldpremportdesc || "-"}</td>
                {/* Render MAC addresses */}
                <td>{extractMacAddresses(iface.macports)}</td>
                {/* Render MAC manufacturers */}
                <td>{extractManufacturers(iface.macports)}</td>
                {/* Placeholders for IP Address and DNS Name */}
                <td></td>
                <td></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ConnectionDetails;
