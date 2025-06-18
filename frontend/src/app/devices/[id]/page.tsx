"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useParams } from "next/navigation";
import { FiHome } from "react-icons/fi";
import { FiArrowLeft } from "react-icons/fi";

const tabs = [
  { label: "Device Overview", content: "Device Overview" },
  { label: "Connection Details", content: "Connection Details" },
  { label: "Connection Charts", content: "Connection Charts" },
];

export default function DevicePage() {
  const params = useParams();
  const [activeTab, setActiveTab] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const router = useRouter();

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <div
        style={{
          width: sidebarOpen ? 220 : 48,
          background: "#f3f4f6",
          transition: "width 0.2s",
          borderRight: "1px solid #e5e7eb",
          display: "flex",
          flexDirection: "column",
          alignItems: sidebarOpen ? "flex-start" : "center",
          padding: "8px 0",
        }}
      >
        {/* Sidebar Toggle */}
        <button
          onClick={() => setSidebarOpen((open) => !open)}
          style={{
            margin: "8px",
            background: "none",
            border: "none",
            cursor: "pointer",
            fontSize: "1.2rem",
            alignSelf: "flex-end",
          }}
          aria-label={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
        >
          {sidebarOpen ? "⏴" : "⏵"}
        </button>
        {sidebarOpen && (
          <>
            <div style={{ margin: "16px", fontWeight: 600 }}>
              <h1>Device {params.id}</h1>
            </div>
            <div style={{ width: "100%" }}>
              {tabs.map((tab, idx) => (
                <button
                  key={tab.label}
                  onClick={() => setActiveTab(idx)}
                  style={{
                    display: "block",
                    width: "100%",
                    padding: "12px 24px",
                    background: activeTab === idx ? "#e0e7ff" : "none",
                    border: "none",
                    borderLeft:
                      activeTab === idx
                        ? "4px solid #2563eb"
                        : "4px solid transparent",
                    color: activeTab === idx ? "#2563eb" : "#374151",
                    fontWeight: activeTab === idx ? 600 : 400,
                    cursor: "pointer",
                    outline: "none",
                    textAlign: "left",
                    fontSize: "1rem",
                  }}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Main Content */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          position: "relative",
        }}
      >
        {/* Home Icon at Top Right */}
        <button
          onClick={() => router.push("/")}
          aria-label="Go to home"
          style={{
            position: "absolute",
            top: 16,
            right: 24,
            background: "none",
            border: "none",
            cursor: "pointer",
            fontSize: "2rem",
            color: "#374151",
            zIndex: 1,
          }}
        >
          <FiHome />
        </button>
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "2rem",
            color: "#6b7280",
            background: "#fff",
          }}
        >
          {tabs[activeTab].content}
        </div>
      </div>
    </div>
  );
}
