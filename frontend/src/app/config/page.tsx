"use client";

import { useEffect, useState } from "react";
import { Sidebar } from "../components/Sidebar";

type Config = any;

export default function ConfigPage() {
  const [config, setConfig] = useState<Config | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState<"zones" | "snmp" | "advanced">(
    "zones"
  );
  const [editingZones, setEditingZones] = useState<Record<number, boolean>>({});

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const res = await fetch("http://localhost:7000/switchmap/api/config", {
          credentials: "include",
        });
        const data = await res.json();
        setConfig(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);

  const handleSave = async () => {
    if (!config) return;
    setSaving(true);
    try {
      await fetch("http://localhost:7000/switchmap/api/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
      });
      alert("Config saved!");
    } catch (err) {
      alert("Failed to save config");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (!config) return <div className="p-4">No config loaded</div>;

  return (
    <div className="flex h-screen overflow-y-auto">
      <Sidebar />
      <div className="p-6 w-full">
        <h1 className="text-2xl font-bold mb-4">Switchmap Config</h1>

        {/* Tabs */}
        <div className="flex border-b mb-4">
          {["zones", "snmp", "advanced"].map((tab) => (
            <button
              key={tab}
              className={`px-4 py-2 -mb-px border-b-2 font-semibold ${
                activeTab === tab
                  ? "border-b-2 border-primary text-primary"
                  : "text-gray-500 hover:text-primary"
              }`}
              onClick={() => setActiveTab(tab as any)}
            >
              {tab === "snmp"
                ? "SNMP Groups"
                : tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === "zones" && (
          <div className="space-y-4">
            {config.poller?.zones?.map((zone: any, idx: number) => {
              const editing = editingZones[idx] || false;

              return (
                <div key={idx} className="space-y-1 border rounded p-3">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold">{zone.zone}</span>
                    <div className="space-x-2">
                      <button
                        className="px-2 py-1 bg-button-bg rounded"
                        onClick={() =>
                          setEditingZones({ ...editingZones, [idx]: !editing })
                        }
                      >
                        {editing ? "Cancel" : "Edit"}
                      </button>
                      <button
                        className="px-2 py-1 border rounded"
                        onClick={() => {
                          const newZones = [...config.poller.zones];
                          newZones.splice(idx, 1);
                          setConfig({
                            ...config,
                            poller: { ...config.poller, zones: newZones },
                          });

                          // Remove from editing state if present
                          const newEditing = { ...editingZones };
                          delete newEditing[idx];
                          setEditingZones(newEditing);
                        }}
                      >
                        Delete
                      </button>
                    </div>
                  </div>

                  {editing ? (
                    <div className="space-y-2">
                      {zone.hostnames.map((host: string, hIdx: number) => (
                        <div key={hIdx} className="flex items-center space-x-2">
                          <input
                            className="border p-1 rounded flex-1"
                            value={host}
                            onChange={(e) => {
                              const newZones = [...config.poller.zones];
                              newZones[idx].hostnames[hIdx] = e.target.value;
                              setConfig({
                                ...config,
                                poller: { ...config.poller, zones: newZones },
                              });
                            }}
                          />
                          <button
                            className="px-2 py-1 border rounded"
                            onClick={() => {
                              const newZones = [...config.poller.zones];
                              newZones[idx].hostnames.splice(hIdx, 1);
                              setConfig({
                                ...config,
                                poller: { ...config.poller, zones: newZones },
                              });
                            }}
                          >
                            Delete
                          </button>
                        </div>
                      ))}
                      <button
                        className="px-2 py-1 bg-green-600 text-white rounded"
                        onClick={() => {
                          const newZones = [...config.poller.zones];
                          newZones[idx].hostnames.push("");
                          setConfig({
                            ...config,
                            poller: { ...config.poller, zones: newZones },
                          });
                        }}
                      >
                        + Add Device
                      </button>
                    </div>
                  ) : (
                    <div>
                      {zone.hostnames.length > 0
                        ? zone.hostnames[0] +
                          (zone.hostnames.length > 1
                            ? ` (+${zone.hostnames.length - 1} more)`
                            : "")
                        : "No devices"}
                    </div>
                  )}
                </div>
              );
            })}
            <button
              className="px-3 py-1 bg-green-600 text-white rounded"
              onClick={() =>
                setConfig({
                  ...config,
                  poller: {
                    ...config.poller,
                    zones: [
                      ...(config.poller.zones || []),
                      { zone: "", hostnames: [] },
                    ],
                  },
                })
              }
            >
              + Add Zone
            </button>
          </div>
        )}

        {activeTab === "snmp" && (
          <div className="space-y-4">
            {config.poller?.snmp_groups?.map((grp: any, idx: number) => (
              <div key={idx} className="space-y-1 border rounded p-3">
                <input
                  className="w-full border p-2 rounded"
                  value={grp.group_name}
                  placeholder="Group Name"
                  onChange={(e) => {
                    const newGroups = [...config.poller.snmp_groups];
                    newGroups[idx].group_name = e.target.value;
                    setConfig({
                      ...config,
                      poller: { ...config.poller, snmp_groups: newGroups },
                    });
                  }}
                />
                <input
                  className="w-full border p-2 rounded"
                  value={grp.snmp_ip || ""}
                  placeholder="IP Address"
                  onChange={(e) => {
                    const newGroups = [...config.poller.snmp_groups];
                    newGroups[idx].snmp_ip = e.target.value;
                    setConfig({
                      ...config,
                      poller: { ...config.poller, snmp_groups: newGroups },
                    });
                  }}
                />
                <label className="inline-flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={grp.enabled || false}
                    onChange={(e) => {
                      const newGroups = [...config.poller.snmp_groups];
                      newGroups[idx].enabled = e.target.checked;
                      setConfig({
                        ...config,
                        poller: { ...config.poller, snmp_groups: newGroups },
                      });
                    }}
                  />
                  <span>Enabled</span>
                </label>
              </div>
            ))}
            <button
              className="px-3 py-1 bg-green-600 text-white rounded"
              onClick={() =>
                setConfig({
                  ...config,
                  poller: {
                    ...config.poller,
                    snmp_groups: [
                      ...(config.poller.snmp_groups || []),
                      { group_name: "", snmp_ip: "", enabled: true },
                    ],
                  },
                })
              }
            >
              + Add SNMP Group
            </button>
          </div>
        )}

        {activeTab === "advanced" && (
          <div className="space-y-4">
            {["core", "server"].map((section) => (
              <details key={section} className="border rounded p-4">
                <summary className="cursor-pointer font-semibold">
                  {section.charAt(0).toUpperCase() + section.slice(1)}
                </summary>
                <div className="mt-2 space-y-2">
                  {Object.entries(config[section]).map(([key, value]) => (
                    <div key={key} className="flex items-center space-x-2">
                      <label className="w-40">{key}:</label>
                      <input
                        className="border p-1 rounded flex-1"
                        type={
                          key.toLowerCase().includes("pass")
                            ? "password"
                            : "text"
                        }
                        value={value as any}
                        onChange={(e) =>
                          setConfig({
                            ...config,
                            [section]: {
                              ...config[section],
                              [key]: e.target.value,
                            },
                          })
                        }
                      />
                    </div>
                  ))}
                </div>
              </details>
            ))}
          </div>
        )}

        <button
          onClick={handleSave}
          disabled={saving}
          className="px-4 py-2 bg-blue-600 text-white rounded mt-4"
        >
          {saving ? "Saving..." : "Save Config"}
        </button>
      </div>
    </div>
  );
}
