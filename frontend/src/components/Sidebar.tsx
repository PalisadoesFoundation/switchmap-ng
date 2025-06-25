import React from "react";
import Link from "next/link";
import { FiLayout, FiClock, FiSettings } from "react-icons/fi";
import ThemeToggle from "@/app/theme-toggle";

export default function Sidebar() {
  return (
    <aside className="sticky top-0 left-0 w-60 h-screen py-8 px-4 border-r border-border">
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
  );
}
