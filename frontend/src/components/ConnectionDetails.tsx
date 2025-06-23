"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import styles from "./ConnectionDetails.module.css";

const QUERY = `
  query Device($id: ID!) {
    device(id: $id) {
      l1interfaces {
        edges {
          node {
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

function ConnectionDetails({ deviceId }: { deviceId?: string }) {
  const params = useParams();
  const id =
    deviceId ??
    (typeof params?.id === "string"
      ? decodeURIComponent(params.id)
      : Array.isArray(params?.id)
      ? decodeURIComponent(params.id[0])
      : undefined);

  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      .then((json) => {
        if (json.errors) throw new Error(json.errors[0].message);
        setData(json.data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (!id) return <p>Error: No device ID provided.</p>;
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!data) return null;
  if (!data.device || !data.device.l1interfaces)
    return <p>No interface data available.</p>;

  const interfaces = data.device.l1interfaces.edges.map(
    ({ node }: any) => node
  );

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Connection Details</h2>
      <table className={styles.detailsTable}>
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
          {interfaces.map((iface: any) => (
            <tr key={iface.idxDevice + iface.ifname}>
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
              <td>{"—"}</td>
              <td>{"—"}</td>
              <td>{"—"}</td>
              <td>{"—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ConnectionDetails;
