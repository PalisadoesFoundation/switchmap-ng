"use client";

import Link from "next/link";
import ThemeToggle from "@/app/theme-toggle";
import styles from "./Home.module.css";
import { FiClock, FiLayout, FiSettings } from "react-icons/fi";
import DevicesOverview from "@/components/DevicesOverview";
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    const hash = window.location.hash;
    if (hash) {
      const el = document.querySelector(hash);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, []);
  return (
    <div className={styles.pageContainer}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <nav>
          <div className={styles.titleContainer}>
            <h2>SwitchMap-NG</h2>
            <ThemeToggle />
          </div>

          <ul style={{ listStyle: "none" }}>
            <li>
              <div className={styles.dashboardLink}>
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
              <div className={styles.dashboardLink}>
                <FiClock className="icon" />
                <Link href="/history">History</Link>
              </div>
            </li>
            <li>
              <div className={styles.dashboardLink}>
                <FiSettings className="icon" />
                <Link href="/settings">Settings</Link>
              </div>
            </li>
          </ul>
        </nav>
      </aside>
      {/* Main Content */}
      <main style={{ overflowY: "auto", flex: 1 }}>
        <div id="network-topology" className={styles.deviceSection}>
          <h2>Network Topology</h2>
        </div>
        <div id="devices-overview" className={styles.deviceSection}>
          <DevicesOverview />
        </div>
      </main>
    </div>
  );
}
