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

  console.log("Macports Data:", macportsData);
  if (!id) return <p>Error: No device ID provided.</p>;
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!deviceData || !macportsData) return null;
  if (!deviceData.device || !deviceData.device.l1interfaces)
    return <p>No interface data available.</p>;

  const interfaces = deviceData.device.l1interfaces.edges.map(
    ({ node }: any) => node
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
    <div className="w-full">
      <h2>Connection Details</h2>
      <table className="mt-20 w-full overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
        <thead>
          <tr>
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
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default ConnectionDetails;
