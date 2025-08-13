"use client";
import React, { useState, useEffect, useMemo } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Sidebar } from "../components/Sidebar";

const QUERY = `
  query ZonesWithDevices {
    zones {
      edges {
        node {
          idxZone
          name
          devices {
            edges {
              node {
                idxDevice
                hostname
                sysName
                lastPolled
              }
            }
          }
        }
      }
    }
  }
`;

type DeviceNode = {
  idxDevice: number;
  hostname: string;
  sysName: string;
  zone?: string;
  lastPolled?: number; // UNIX timestamp in seconds
};

export default function DeviceHistoryChart() {
  const [allDevices, setAllDevices] = useState<DeviceNode[]>([]);
  const [inputTerm, setInputTerm] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDevices() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(
          process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: QUERY }),
          }
        );
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (json.errors) throw new Error(json.errors[0].message);

        // Flatten zones and devices, adding zone name to device
        const zones = json.data.zones.edges;
        const devicesWithZones: DeviceNode[] = [];
        zones.forEach(({ node: zone }: any) => {
          zone.devices.edges.forEach(({ node: device }: any) => {
            devicesWithZones.push({
              ...device,
              zone: zone.name,
            });
          });
        });

        setAllDevices(devicesWithZones);

        // Set first device by default
        if (devicesWithZones.length > 0) {
          setSearchTerm(devicesWithZones[0].hostname);
        }
      } catch (err: any) {
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    }
    fetchDevices();
  }, []);

  const uniqueHostnames = useMemo(() => {
    return Array.from(new Set(allDevices.map((d) => d.hostname)));
  }, [allDevices]);

  useEffect(() => {
    if (inputTerm.trim() === "") {
      setSuggestions([]);
      return;
    }
    const filtered = uniqueHostnames
      .filter((host) => host.toLowerCase().includes(inputTerm.toLowerCase()))
      .slice(0, 5);
    setSuggestions(filtered);
  }, [inputTerm, uniqueHostnames]);

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (inputTerm.trim() === "") return;
    setSearchTerm(inputTerm);
    setInputTerm("");
    setSuggestions([]);
  }

  // Sort using lastPolled (converted to ms)
  const history = allDevices
    .filter((d) => d.hostname === searchTerm && d.lastPolled)
    .sort((a, b) => (a.lastPolled ?? 0) * 1000 - (b.lastPolled ?? 0) * 1000);

  // SysName data
  const sysNameCategories = Array.from(new Set(history.map((h) => h.sysName)));
  const sysNameMap: Record<string, number> = {};
  sysNameCategories.forEach((name, i) => {
    sysNameMap[name] = i + 1;
  });
  const sysNameChartData = history.map((h) => ({
    timestamp: new Date((h.lastPolled ?? 0) * 1000).toISOString(),
    sysNameNum: sysNameMap[h.sysName],
    sysName: h.sysName,
  }));

  // Zone data
  const zoneCategories = Array.from(
    new Set(history.map((h) => h.zone || ""))
  ).filter(Boolean);
  const zoneMap: Record<string, number> = {};
  zoneCategories.forEach((zone, i) => {
    zoneMap[zone] = i + 1;
  });
  const zoneChartData = history
    .filter((h) => h.zone)
    .map((h) => ({
      timestamp: new Date((h.lastPolled ?? 0) * 1000).toISOString(),
      zoneNum: zoneMap[h.zone || ""],
      zoneName: h.zone || "",
    }));

  return (
    <div className="flex h-screen p-4 max-w-full">
      <Sidebar />
      <div className="p-4 w-full max-w-full flex flex-col gap-6 h-full overflow-y-auto ml-10">
        <div>
          <h2 className="text-xl font-semibold">Device History</h2>
          <p className="text-sm pt-2 text-gray-600">
            Visualizing the historical movement and status changes of devices
            within the network.
          </p>
        </div>

        <div className="relative max-w-sm">
          <form
            className="flex flex-col gap-4 md:flex-row md:items-center"
            onSubmit={onSubmit}
          >
            <input
              className="border p-2 rounded w-full"
              type="text"
              placeholder="Search device hostname..."
              value={inputTerm}
              onChange={(e) => setInputTerm(e.target.value)}
              autoComplete="off"
            />
            <button
              type="submit"
              className="border-2 text-button rounded px-4 py-2 cursor-pointer transition-colors duration-300 align-middle h-fit"
            >
              Search
            </button>
          </form>

          {suggestions.length > 0 && (
            <ul className="absolute bg-bg shadow-md mt-1 rounded border w-full z-50">
              {suggestions.map((suggestion, i) => (
                <li
                  key={i}
                  onClick={() => {
                    setSearchTerm(suggestion);
                    setInputTerm("");
                    setSuggestions([]);
                  }}
                  className="cursor-pointer px-4 py-2 hover:bg-hover-bg"
                >
                  {suggestion}
                </li>
              ))}
            </ul>
          )}

          {loading && (
            <p className="mt-2 text-sm text-gray-500">Loading devices...</p>
          )}
          {error && <p className="mt-2 text-sm text-red-600">Error: {error}</p>}
        </div>
        {searchTerm && (
          <p className="mt-2 text-gray-700">
            Showing results for Hostname:{" "}
            <span className="font-semibold">{searchTerm}</span>
          </p>
        )}

        <div className="overflow-auto">
          <div className="gap-8 w-[70vw] min-w-[600px] items-stretch p-4 mx-auto flex flex-col lg:flex-row lg:text-left text-center ">
            {/* SysName Chart */}
            {sysNameChartData.length > 0 && (
              <div className="w-full h-64 pl-6 flex flex-col">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sysNameChartData} margin={{ right: 20 }}>
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(t) =>
                        new Date(t).toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                        })
                      }
                    />
                    <YAxis
                      type="number"
                      domain={[0, sysNameCategories.length + 1]}
                      ticks={Object.values(sysNameMap)}
                      tickFormatter={(v) =>
                        sysNameCategories.find(
                          (name) => sysNameMap[name] === v
                        ) || ""
                      }
                      width={200}
                      tick={{ textAnchor: "end" }}
                    />
                    <Tooltip
                      labelFormatter={(label) =>
                        new Date(label).toLocaleString()
                      }
                      formatter={(_, __, props) => [
                        props.payload.sysName,
                        "SysName",
                      ]}
                    />
                    <Line
                      type="stepAfter"
                      dataKey="sysNameNum"
                      stroke="#3b82f6"
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>

                <h3 className="text-lg font-semibold mt-4 text-center">
                  SysName History
                </h3>
              </div>
            )}

            {/* Zone Chart */}
            {zoneChartData.length > 0 && (
              <div className="w-full h-64 pl-6 flex flex-col">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={zoneChartData} margin={{ right: 20 }}>
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(t) =>
                        new Date(t).toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                        })
                      }
                    />
                    <YAxis
                      type="number"
                      domain={[0, zoneCategories.length + 1]}
                      ticks={Object.values(zoneMap)}
                      tickFormatter={(v) =>
                        zoneCategories.find((zone) => zoneMap[zone] === v) || ""
                      }
                      width={200}
                      tick={{ textAnchor: "end" }}
                    />
                    <Tooltip
                      labelFormatter={(label) =>
                        new Date(label).toLocaleString()
                      }
                      formatter={(_, __, props) => [
                        props.payload.zoneName,
                        "Zone",
                      ]}
                    />
                    <Line
                      type="stepAfter"
                      dataKey="zoneNum"
                      stroke="#16a34a"
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>

                <h3 className="text-lg font-semibold mt-4 text-center">
                  Zone History
                </h3>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
