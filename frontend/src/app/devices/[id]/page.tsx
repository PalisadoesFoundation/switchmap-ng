"use client";
import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";
import { FiHome, FiMonitor, FiLink, FiBarChart2 } from "react-icons/fi";
import ThemeToggle from "@/app/theme-toggle";
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
    <div className="flex h-screen">
      {/* Sidebar */}
      <div
        className="transition-width duration-200 border-r border-[var(--border-color)] flex flex-col gap-4 py-2"
        style={{
          width: sidebarOpen ? "220px" : "48px",
          alignItems: sidebarOpen ? "flex-start" : "center",
        }}
      >
        <div
          className={
            sidebarOpen
              ? "flex flex-row-reverse justify-between w-[95%] self-end mb-8"
              : "flex flex-col gap-4 mb-8"
          }
        >
          {/* Sidebar Toggle */}
          <button
            className="my-2 px-0 bg-transparent text-[1.2rem] self-center"
            onClick={() => setSidebarOpen((open) => !open)}
            aria-label={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
          >
            {sidebarOpen ? "⏴" : "⏵"}
          </button>
          <ThemeToggle />
        </div>
        <div className="flex flex-col items-center">
          <h1
            className={`px-4 py-3 text-[1.2rem] max-w-[150px] break-all whitespace-normal overflow-hidden
  
 ${!sidebarOpen ? "hidden" : ""}`}
          >
            {sysName || hostname || "Unnamed Device"}
          </h1>
        </div>
        <div className="w-full flex flex-col">
          {tabs.map((tab, idx) => (
            <button
              key={tab.label}
              onClick={() => setActiveTab(idx)}
              className={`bg-transparent px-4 py-3 font-normal text-left text-base
 ${activeTab === idx ? "bg-[var(--select-bg)]" : ""}`}
            >
              <span className="flex flex-row gap-4">
                {tab.icon}
                {sidebarOpen && <span>{tab.label}</span>}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative" style={{ width: "80vw" }}>
        {/* Home Icon at Top Right */}
        <button
          onClick={() => router.push("/")}
          aria-label="Go to home"
          className="absolute top-4 right-6 bg-transparent text-[1.2rem]"
        >
          <FiHome />
        </button>
        <div className="max-w-full flex items-center justify-center w-full h-full">
          {tabs[activeTab].content}
        </div>
      </div>
    </div>
  );
}
