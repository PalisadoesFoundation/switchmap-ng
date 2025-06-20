"useclient";

import Link from "next/link";
import ThemeToggle from "./theme-toggle";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <nav style={{ position: "sticky", top: 0 }}>
          <h2>SwitchMap-NG</h2>
          <ThemeToggle />
          <ul style={{ listStyle: "none" }}>
            <li>
              <strong>Dashboard</strong>
              <ul style={{ listStyle: "none" }}>
                <li>
                  <Link href="#network-topology">Network Topology</Link>
                </li>
                <li>
                  <Link href="#devices-overview">Devices Overview</Link>
                </li>
              </ul>
            </li>
            <li>
              <Link href="/history">History</Link>
            </li>
            <li style={{ marginTop: "1.5rem" }}>
              <Link href="/settings">Settings</Link>
            </li>
          </ul>
        </nav>
      </aside>
      {/* Main Content */}
      <main style={{ overflowY: "auto", flex: 1 }}>
        <div
          id="network-topology"
          style={{ height: "100vh", marginBottom: "2rem", padding: "2rem" }}
        >
          <p>Network Topology</p>
        </div>
        <div
          id="devices-overview"
          style={{ height: "100vh", marginBottom: "2rem", padding: "2rem" }}
        >
          <p>Devices Overview</p>
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              marginTop: "1rem",
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    borderBottom: "1px solid #ccc",
                    textAlign: "left",
                    padding: "0.5rem",
                  }}
                >
                  Device Name
                </th>
                <th
                  style={{
                    borderBottom: "1px solid #ccc",
                    textAlign: "left",
                    padding: "0.5rem",
                  }}
                >
                  IP Address
                </th>
                <th
                  style={{
                    borderBottom: "1px solid #ccc",
                    textAlign: "left",
                    padding: "0.5rem",
                  }}
                >
                  Device Type
                </th>
                <th
                  style={{
                    borderBottom: "1px solid #ccc",
                    textAlign: "left",
                    padding: "0.5rem",
                  }}
                >
                  Active Port
                </th>
                <th
                  style={{
                    borderBottom: "1px solid #ccc",
                    textAlign: "left",
                    padding: "0.5rem",
                  }}
                >
                  Uptime
                </th>
              </tr>
            </thead>
            <tbody>
              {/* Example static data, replace with dynamic data as needed */}
              {[
                {
                  id: "1",
                  name: "Switch Alpha",
                  ip: "192.168.1.10",
                  type: "Layer 2 Switch",
                  activePort: "4/4",
                  uptime: "12d 4h",
                },
                {
                  id: "2",
                  name: "Router Beta",
                  ip: "192.168.1.1",
                  type: "Router",
                  activePort: "2/4",
                  uptime: "7d 18h",
                },
                {
                  id: "3",
                  name: "Switch Gamma",
                  ip: "192.168.1.11",
                  type: "Layer 3 Switch",
                  activePort: "3/4",
                  uptime: "22d 2h",
                },
              ].map((device) => (
                <tr key={device.id}>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    <Link href={`/devices/${device.id}`}>{device.name}</Link>
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    {device.ip}
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    {device.type}
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    {device.activePort}
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #eee",
                    }}
                  >
                    {device.uptime}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
