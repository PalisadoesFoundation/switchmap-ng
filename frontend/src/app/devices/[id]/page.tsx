"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useParams } from "next/navigation";
import { FiHome, FiMonitor, FiLink, FiBarChart2 } from "react-icons/fi";
import ThemeToggle from "@/app/theme-toggle";
import styles from "./devices.module.css";

const tabs = [
  {
    label: "Device Overview",
    content: "Device Overview",
    icon: <FiMonitor />,
  },
  {
    label: "Connection Details",
    content: "Connection Details",
    icon: <FiLink />,
  },
  {
    label: "Connection Charts",
    content: "Connection Charts",
    icon: <FiBarChart2 />,
  },
];

export default function DevicePage() {
  const params = useParams();
  const [activeTab, setActiveTab] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const router = useRouter();

  return (
    <div className={styles.devicePage}>
      {/* Sidebar */}
      <div
        className={styles.sidebar}
        style={{
          width: sidebarOpen ? "220px" : "48px",
          alignItems: sidebarOpen ? "flex-start" : "center",
        }}
      >
        <div
          className={
            sidebarOpen ? styles.sidebarHeader : styles.sidebarHeaderCollapsed
          }
        >
          {/* Sidebar Toggle */}
          <button
            className={styles.sidebarToggle}
            onClick={() => setSidebarOpen((open) => !open)}
            aria-label={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
          >
            {sidebarOpen ? "⏴" : "⏵"}
          </button>
          <ThemeToggle />
        </div>
        {sidebarOpen && <h1>Device {params.id}</h1>}
        <div className={styles.tabs}>
          {tabs.map((tab, idx) => (
            <button
              key={tab.label}
              onClick={() => setActiveTab(idx)}
              className={`${styles.tabButton} ${
                activeTab === idx ? styles.activeTab : ""
              }`}
            >
              <span className={styles.tabContent}>
                {tab.icon}
                {sidebarOpen && <span>{tab.label}</span>}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Home Icon at Top Right */}
        <button
          onClick={() => router.push("/")}
          aria-label="Go to home"
          className={styles.homeButton}
        >
          <FiHome />
        </button>
        <div className={styles.tabSection}>{tabs[activeTab].content}</div>
      </div>
    </div>
  );
}
