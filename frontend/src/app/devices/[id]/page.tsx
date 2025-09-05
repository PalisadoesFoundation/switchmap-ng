"use client";
import React, { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { FiHome, FiMonitor, FiLink, FiBarChart2 } from "react-icons/fi";
import { ThemeToggle } from "@/app/theme-toggle";
import { ConnectionDetails } from "@/app/components/ConnectionDetails";
import { DeviceDetails } from "@/app/components/DeviceDetails";
import { DeviceNode } from "@/app/types/graphql/GetZoneDevices";

/** * Represents a tab item with label, content, and icon.
 * @remarks
 * - `label`: The display label of the tab.
 * - `content`: The React node to be rendered when the tab is active.
 * - `icon`: The icon associated with the tab.
 * @returns {TabItem} An object representing a tab item.
 * @see {@link TabItem}
 * @interface TabItem
 * @property {string} label - The label of the tab.
 * @property {React.ReactNode} content - The content to display when the tab is active.
 * @property {React.ReactElement} icon - The icon representing the tab.
 */
interface TabItem {
  label: string;
  content: React.ReactNode;
  icon: React.ReactElement;
}

const QUERY = `
  query Device($id: ID!) {
    device(id: $id) {
      id
      idxDevice
      sysObjectid
      sysUptime
      sysDescription
      sysName
      hostname
      lastPolled
      l1interfaces {
        edges {
          node {
            idxL1interface
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
            macports {
              edges {
                node {
                  macs {
                    mac
                    oui {
                      organization
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
`;

export default function DevicePage() {
  const params = useParams<{ id: string | string[] }>();
  const searchParams = useSearchParams();
  const sysName = searchParams.get("sysName") ?? "";
  const hostname = searchParams.get("hostname") ?? "";

  const id = Array.isArray(params.id) ? params.id[0] : params.id;
  const [device, setDevice] = useState<DeviceNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleTabChange = (idx: number) => {
    const params = new URLSearchParams(window.location.search);
    params.set("tab", String(idx));
    const hash = window.location.hash;
    router.replace(`${window.location.pathname}?${params.toString()}${hash}`);
    setActiveTab(idx);
  };

  useEffect(() => {
    if (!id) return;
    const globalId = btoa(`Device:${id}`);
    setLoading(true);
    setError(null);

    fetch(
      process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
        "http://localhost:7000/switchmap/api/graphql",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: QUERY, variables: { id: globalId } }),
      }
    )
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        if (json.errors) throw new Error(json.errors[0].message);
        setDevice(json.data.device);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  const tabs: TabItem[] = [
    {
      label: "Device Overview",
      content: loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : device ? (
        <DeviceDetails device={device} />
      ) : (
        <p>No device data.</p>
      ),
      icon: <FiMonitor className="icon" />,
    },
    {
      label: "Connection Details",
      content: loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : device ? (
        <ConnectionDetails device={device} />
      ) : (
        <p>No device data.</p>
      ),
      icon: <FiLink className="icon" />,
    },
    {
      label: "Connection Charts",
      content: <div>Connection Charts</div>,
      icon: <FiBarChart2 className="icon" />,
    },
  ];

  const initialTab = Number(searchParams.get("tab") ?? 0);
  const [activeTab, setActiveTab] = useState(initialTab);
  const [sidebarOpen, setSidebarOpen] = useState<boolean | null>(null);

  useEffect(() => {
    const media = window.matchMedia("(min-width: 1024px)");
    const handler = () => setSidebarOpen(media.matches);

    handler();
    media.addEventListener("change", handler);

    return () => media.removeEventListener("change", handler);
  }, []);

  if (sidebarOpen === null) return null;

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
            className={`px-4 py-3 text-[1.2rem] max-w-[150px] break-all whitespace-normal overflow-hidden ${
              !sidebarOpen ? "hidden" : ""
            }`}
          >
            {sysName || hostname || "Unnamed Device"}
          </h1>
        </div>
        <div className="w-full flex flex-col">
          {tabs.map((tab, idx) => (
            <button
              key={tab.label}
              onClick={() => handleTabChange(idx)}
              className={`bg-transparent px-4 py-3 font-normal text-left text-base ${
                activeTab === idx ? "bg-[var(--select-bg)]" : ""
              }`}
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
        <button
          onClick={() => router.push("/")}
          aria-label="Go to home"
          className="absolute top-4 right-6 bg-transparent text-[1.2rem]"
        >
          <FiHome />
        </button>
        <div className="max-w-full flex items-center justify-center w-full h-full overflow-y-auto">
          {tabs[activeTab].content}
        </div>
      </div>
    </div>
  );
}
