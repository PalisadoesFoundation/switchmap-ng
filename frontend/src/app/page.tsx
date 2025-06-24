"use client";

import Link from "next/link";
import ThemeToggle from "@/app/theme-toggle";
import { FiClock, FiLayout, FiSettings } from "react-icons/fi";
import DevicesOverview from "@/app/components/DevicesOverview";
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
    <div className="flex flex-row h-screen overflow-y-hidden">
      {/* Sidebar */}
      <aside className="sticky top-0 left-0 w-60 h-screen py-8 px-4 border-r border-[var(--border-color)]">
        <nav>
          <div className="flex flex-row gap-4">
            <h2>SwitchMap-NG</h2>
            <ThemeToggle />
          </div>

          <ul style={{ listStyle: "none" }}>
            <li>
              <div className="flex flex-row items-center gap-2">
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
              <div className="flex flex-row items-center gap-2">
                <FiClock className="icon" />
                <Link href="/history">History</Link>
              </div>
            </li>
            <li>
              <div className="flex flex-row items-center gap-2">
                <FiSettings className="icon" />
                <Link href="/settings">Settings</Link>
              </div>
            </li>
          </ul>
        </nav>
      </aside>
      {/* Main Content */}
      <main style={{ overflowY: "auto", flex: 1 }}>
        <div id="network-topology" className="h-screen mb-8 p-8">
          <h2>Network Topology</h2>
        </div>
        <div id="devices-overview" className="h-screen mb-8 p-8">
          <DevicesOverview />
        </div>
      </main>
    </div>
  );
}
