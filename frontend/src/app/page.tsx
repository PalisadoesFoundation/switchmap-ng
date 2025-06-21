"useclient";

import Link from "next/link";
import ThemeToggle from "./theme-toggle";
import styles from "./page.module.css";
import { FiClock, FiLayout, FiSettings } from "react-icons/fi";

export default function Home() {
  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <nav style={{ position: "sticky", top: 0 }}>
          <div className={styles["title-container"]}>
            <h2>SwitchMap-NG</h2>
            <ThemeToggle />
          </div>

          <ul style={{ listStyle: "none" }}>
            <li>
              <div className={styles["dashboard-link"]}>
                <FiLayout className="icon" />
                <p>Dashboard</p>
              </div>

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
              <div className={styles["dashboard-link"]}>
                <FiClock className="icon" />
                <Link href="/history">History</Link>
              </div>
            </li>
            <li>
              <div className={styles["dashboard-link"]}>
                <FiSettings className="icon" />
                <Link href="/settings">Settings</Link>
              </div>
            </li>
          </ul>
        </nav>
      </aside>
      {/* Main Content */}
      <main style={{ overflowY: "auto", flex: 1 }}>
        <div id="network-topology" className={styles["device-section"]}>
          <p>Network Topology</p>
        </div>
        <div id="devices-overview" className={styles["device-section"]}>
          <p>Devices Overview</p>
          <table>
            <thead>
              <tr>
                <th>Device Name</th>
                <th>IP Address</th>
                <th>Device Type</th>
                <th>Active Port</th>
                <th>Uptime</th>
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
                  <td>{device.ip}</td>
                  <td>{device.type}</td>
                  <td>{device.activePort}</td>
                  <td>{device.uptime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
