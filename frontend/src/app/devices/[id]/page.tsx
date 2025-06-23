"use client";
import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";
import { FiHome, FiMonitor, FiLink, FiBarChart2 } from "react-icons/fi";
import ThemeToggle from "@/app/theme-toggle";
import styles from "./Devices.module.css";
import ConnectionDetails from "@/components/ConnectionDetails";

export default function DevicePage() {
  const searchParams = useSearchParams();
  const sysName = searchParams.get("sysName");
  const hostname = searchParams.get("hostname");
  const params = useParams();
  // Ensure id is always a string
  const id = Array.isArray(params.id) ? params.id[0] : params.id;

  const tabs = [
    {
      label: "Device Overview",
      content: <div>Device Overview</div>,
      icon: <FiMonitor className="icon" />,
    },
    {
      label: "Connection Details",
      content: <ConnectionDetails deviceId={id || ""} />,
      icon: <FiLink className="icon" />,
    },
    {
      label: "Connection Charts",
      content: <div>Connection Charts</div>,
      icon: <FiBarChart2 className="icon" />,
    },
  ];
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
        <h1
          className={`${styles.deviceName} ${
            !sidebarOpen ? styles.deviceNameCollapsed : ""
          }`}
        >
          {sysName || hostname || "Unnamed Device"}
        </h1>
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
