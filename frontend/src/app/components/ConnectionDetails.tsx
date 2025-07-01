"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

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
          }
        }
      }
    }
  }
`;
const MACPORTS_QUERY = (ids: number[]) => `
  {
    macports(filter: { idxL1interface: { in: [${ids.join(",")}] } }) {
      edges {
        node {
          id
          idxMac
          idxL1interface
          macs {
            mac
            oui {
              organization
            }
          }
        }
      }
    }
  }
`;
const MACIPS_QUERY = (ids: number[]) => `
  {
    macips(filter: { idxMac: { in: [${ids.join(",")}] } }) {
      edges {
        node {
          id
          idxMac
          ips {
            address
            hostname
          }
          macs {
            idxMac
          }
        }
      }
    }
  }
`;

function ConnectionDetails({ deviceId }: { deviceId?: string }) {
  const params = useParams();
  const id =
    deviceId ??
    (typeof params?.id === "string"
      ? decodeURIComponent(params.id)
      : Array.isArray(params?.id)
      ? decodeURIComponent(params.id[0])
      : undefined);

  const [deviceData, setDeviceData] = useState<any>(null);
  const [macportsData, setMacportsData] = useState<any>(null);
  const [macipsData, setMacipsData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    const globalId = id && typeof id === "string" ? btoa(`Device:${id}`) : id;

    fetch("http://localhost:7000/switchmap/api/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: QUERY, variables: { id: globalId } }),
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

        if (idxL1interfaces.length === 0) {
          setMacportsData({ macports: { edges: [] } });
          return null;
        }
        const query = MACPORTS_QUERY(idxL1interfaces.map(Number));

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
        if (macportsJson.errors)
          throw new Error(macportsJson.errors[0].message);
        setMacportsData(macportsJson.data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);
  console.log("Setting up second useEffect — macportsData:", macportsData);

  useEffect(() => {
    if (!macportsData) {
      console.log("macportsData is null or undefined — skipping IP fetch");
      return;
    }

    console.log("macportsData available:", macportsData);

    const macIds = macportsData.macports.edges
      .map((edge: any) => edge.node.idxMac)
      .filter((id: any) => id !== undefined && id !== null);

    console.log("MAC IDs for IP fetch:", macIds);

    if (macIds.length === 0) {
      console.log("No MACs found, skipping IP query.");
      return;
    }

    const query = MACIPS_QUERY(macIds.map(Number));

    fetch("http://localhost:7000/switchmap/api/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    })
      .then((res) => res.json())
      .then((macipsJson) => {
        setMacipsData(macipsJson.data);
        console.log("MAC-IP data fetched:", macipsJson.data);
      })
      .catch((err) => console.error("MAC-IP fetch error:", err));
  }, [macportsData]);

  if (!id) return <p>Error: No device ID provided.</p>;
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!deviceData || !macportsData) return null;
  if (!deviceData.device || !deviceData.device.l1interfaces)
    return <p>No interface data available.</p>;

  const interfaces = deviceData.device.l1interfaces.edges.map(
    ({ node }: any) => node
  );
  type IpNode = {
    idxMac: number;
    ips?: IpEntry[];
    macs?: { idxMac: number }[];
  };

  const ipNodesByMacIdx = new Map<number, IpNode>(
    (macipsData?.macips?.edges ?? []).map(({ node }: { node: IpNode }) => [
      node.idxMac,
      node,
    ])
  );

  type MacportNode = {
    idxL1interface: number;
    idxMac: number;
    macs?: {
      mac: string;
      oui?: {
        organization?: string;
      };
    };
  };
  type IpEntry = {
    address: string;
    hostname?: string;
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
    <div className="w-[87%] h-[80vh] mt-16">
      <h2>Connection Details</h2>
      <div className="w-full h-full overflow-auto border border-gray-200 ">
        <table
          className="w-full h-full border border-gray-200 rounded-lg shadow-sm"
          style={{ marginTop: "0rem" }}
        >
          <thead>
            <tr className="sticky top-0 bg-bg z-10 border-gray-200">
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
            {interfaces.map((iface: any) => {
              const macport = macportsNodesByIdx.get(iface.idxL1interface);
              const mac = macport?.macs?.mac ?? "—";
              const manufacturer = macport?.macs?.oui?.organization ?? "—";

              // Get IP info from ipNodesByMacIdx using idxMac
              const ipInfo = macport
                ? ipNodesByMacIdx.get(macport.idxMac)
                : null;
              const ip = ipInfo?.ips?.[0]?.address ?? "—";
              const dns = ipInfo?.ips?.[0]?.hostname ?? "—";

              return (
                <tr key={`${iface.idxL1interface}-${iface.ifname}`}>
                  <td>{iface.ifname || "N/A"}</td>
                  <td>{iface.nativevlan ?? "N/A"}</td>
                  <td>{iface.ifoperstatus ?? "N/A"}</td>
                  <td>{iface.tsIdle ?? "N/A"}</td>
                  <td>{iface.ifspeed ?? "N/A"}</td>
                  <td>{iface.duplex ?? "N/A"}</td>
                  <td>{iface.ifalias || "N/A"}</td>
                  <td>{iface.trunk ? "Yes" : "No"}</td>
                  <td>{iface.cdpcachedeviceid || ""}</td>
                  <td>{iface.lldpremportdesc || ""}</td>
                  <td>{mac}</td>
                  <td>{manufacturer}</td>
                  <td>{ip}</td>
                  <td>{dns}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ConnectionDetails;
