"use client";
import React, {
  useState,
  useMemo,
  useCallback,
  useEffect,
  Suspense,
  lazy,
} from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { FiHome, FiMonitor, FiLink, FiBarChart2 } from "react-icons/fi";
import { ThemeToggle } from "@/app/theme-toggle";
import useSWR from "swr";

/**
 * DevicePage component displays detailed information about a specific device.
 *
 * @remarks
 * This component fetches device data based on the device ID from the URL parameters.
 * It provides a sidebar for navigation between different tabs: Device Overview,
 * Connection Details, and Connection Charts. The sidebar can be toggled between
 * these tabs to display the corresponding content.
 * @returns The DevicePage component.
 * @see {@link useSWR} for data fetching and caching.
 * @see {@link ThemeToggle} for theme switching functionality.
 * @see {@link DeviceDetails}, {@link ConnectionDetails}, and {@link ConnectionCharts} for tab content.
 */

const DeviceDetails = lazy(() =>
  import("@/app/components/DeviceDetails").then((m) => ({
    default: m.DeviceDetails,
  }))
);
const ConnectionDetails = lazy(() =>
  import("@/app/components/ConnectionDetails").then((m) => ({
    default: m.ConnectionDetails,
  }))
);
const ConnectionCharts = lazy(() =>
  import("@/app/components/ConnectionCharts").then((m) => ({
    default: m.ConnectionCharts,
  }))
);

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

const fetcher = async (query: string, id: string) => {
  const res = await fetch(
    process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
      "http://localhost:7000/switchmap/api/graphql",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, variables: { id } }),
    }
  );
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const json = await res.json();
  if (json.errors) throw new Error(json.errors[0].message);
  return json.data.device;
};

export default function DevicePage() {
  const params = useParams<{ id: string | string[] }>();
  const searchParams = useSearchParams();
  const router = useRouter();

  const idParam = Array.isArray(params.id) ? params.id[0] : params.id;
  const globalId = idParam ? btoa(`Device:${idParam}`) : null;
  const sysName = searchParams.get("sysName") ?? "";
  const hostname = searchParams.get("hostname") ?? "";

  const {
    data: device,
    error,
    isLoading,
  } = useSWR(
    globalId ? [QUERY, globalId] : null,
    ([query, id]) => fetcher(query, id),
    { revalidateOnFocus: false, dedupingInterval: 300000 }
  );

  const clamp = useCallback(
    (n: number, min: number, max: number) => Math.min(Math.max(n, min), max),
    []
  );

  const parsedTab = Number.parseInt(searchParams.get("tab") ?? "0", 10);
  const [activeTab, setActiveTab] = useState(
    Number.isNaN(parsedTab) ? 0 : clamp(parsedTab, 0, 2)
  );

  const handleTabChange = useCallback(
    (idx: number) => {
      const params = new URLSearchParams(window.location.search);
      params.set("tab", String(idx));
      const hash = window.location.hash;
      router.replace(`${window.location.pathname}?${params.toString()}${hash}`);
      setActiveTab(idx);
    },
    [router]
  );

  const [sidebarOpen, setSidebarOpen] = useState<boolean | null>(null);
  useEffect(() => {
    const media = window.matchMedia("(min-width: 1024px)");
    const handler = () => setSidebarOpen(media.matches);
    handler();
    media.addEventListener("change", handler);
    return () => media.removeEventListener("change", handler);
  }, []);

  const tabs = useMemo(
    () => [
      {
        label: "Device Overview",
        icon: <FiMonitor className="icon" />,
        content: device ? (
          <Suspense fallback={<p>Loading...</p>}>
            <DeviceDetails device={device} />
          </Suspense>
        ) : isLoading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>Error: {error.message}</p>
        ) : (
          <p>No device data.</p>
        ),
      },
      {
        label: "Connection Details",
        icon: <FiLink className="icon" />,
        content: device ? (
          <Suspense fallback={<p>Loading...</p>}>
            <ConnectionDetails device={device} />
          </Suspense>
        ) : isLoading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>Error: {error.message}</p>
        ) : (
          <p>No device data.</p>
        ),
      },
      {
        label: "Connection Charts",
        icon: <FiBarChart2 className="icon" />,
        content: device ? (
          <Suspense fallback={<p>Loading...</p>}>
            <ConnectionCharts device={device} />
          </Suspense>
        ) : isLoading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>Error: {error.message}</p>
        ) : (
          <p>No device data.</p>
        ),
      },
    ],
    [device, error, isLoading]
  );

  if (sidebarOpen === null) return null;

  return (
    <div className="relative">
      {/* Sidebar */}
      <div
        className="fixed top-0 left-0 z-50 h-screen transition-all duration-200 border-r border-[var(--border-color)] flex flex-col gap-4 py-2 bg-sidebar"
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

      {/* Main content */}
      <div
        className="ml-[48px] transition-all duration-200 min-h-screen overflow-y-auto"
        style={{ marginLeft: sidebarOpen ? "220px" : "48px" }}
      >
        <button
          onClick={() => router.push("/")}
          aria-label="Go to home"
          className="absolute top-4 right-6 bg-transparent text-[1.2rem]"
        >
          <FiHome />
        </button>

        <div className="max-w-full flex items-center justify-center min-h-screen">
          {tabs[activeTab]?.content}
        </div>
      </div>
    </div>
  );
}
