"use client";

import { useEffect, useState } from "react";
import { Sidebar } from "../components/Sidebar";
import {
  FiCheck,
  FiEdit2,
  FiMinus,
  FiTrash2,
  FiChevronDown,
  FiChevronUp,
} from "react-icons/fi";

type Config = any;

export default function ConfigPage() {
  const [config, setConfig] = useState<Config | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [draftZone, setDraftZone] = useState<string | null>(null);
  const [editIdx, setEditIdx] = useState<number | null>(null);
  const [editSection, setEditSection] = useState<"core" | "server" | null>(
    null
  );
  const [expandedSections, setExpandedSections] = useState<
    Record<string, boolean>
  >({});

  const [activeTab, setActiveTab] = useState<"zones" | "snmp" | "advanced">(
    "zones"
  );
  const sections: ("core" | "server")[] = ["core", "server"];
  const [editingZones, setEditingZones] = useState<Record<number, boolean>>({});
  const [authPasswordEdit, setAuthPasswordEdit] = useState(false);
  const [expandedZones, setExpandedZones] = useState<Record<number, boolean>>(
    {}
  );

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
    setSaved(false);

    try {
      const res = await fetch("http://localhost:7000/switchmap/api/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
      });

      if (!res.ok) throw new Error("Request failed");

      setSaved(true);

      // hide "Saved!" after 2s
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      console.error(err);
      // optional: show error inline instead of alert
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex h-screen overflow-y-auto">
      <Sidebar />
      <div className="p-4 w-full max-w-full flex flex-col gap-6 h-fit mx-10 min-w-[400px]">
        <div className="m-4 lg:ml-0">
          <h1 className="text-xl font-semibold">Switchmap Config</h1>
          <p className="text-sm pt-2 text-gray-600">
            Manage and customize your Switchmap settings
          </p>
        </div>
        {/* Loading / No config placeholder */}
        {(loading || !config) && (
          <div className="flex-1 flex items-center justify-center text-gray-700">
            {loading ? "Loading…" : "No config loaded"}
          </div>
        )}
        {/* Only render the tabs and content if config exists */}
        {!loading && config && (
          <>
            {/* Tabs */}
            <div className="flex border-b mb-4">
              {["zones", "snmp", "advanced"].map((tab) => (
                <button
                  key={tab}
                  className={`px-4 py-2 -mb-px border-b-2 font-semibold ${
                    activeTab === tab
                      ? "border-b-2 border-primary text-primary hover:bg-hover-bg"
                      : "text-gray-500 hover:bg-hover-bg"
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
                  const expanded = expandedZones[idx];

                  return (
                    <div key={idx} className="space-y-1 border rounded p-3">
                      <div className="mb-4 flex justify-between items-center">
                        <span className="font-semibold">{zone.zone}</span>

                        <div className="space-x-2 flex flex-row items-center">
                          {/* Edit button */}
                          <div className="mr-4 ">
                            <button
                              className={`p-1 mr-1 rounded transition ${
                                editing
                                  ? "bg-purple-500 text-white hover:bg-purple-600"
                                  : "text-primary hover:text-hover-bg"
                              }`}
                              onClick={() => {
                                setEditingZones({
                                  ...editingZones,
                                  [idx]: !editing,
                                });

                                setExpandedZones({
                                  ...expandedZones,
                                  [idx]: true,
                                });
                              }}
                            >
                              {editing ? <FiCheck /> : <FiEdit2 />}
                            </button>

                            {/* Delete button */}
                            <button
                              className="text-primary hover:text-hover-bg"
                              onClick={() => {
                                const newZones = [...config.poller.zones];
                                newZones.splice(idx, 1);
                                setConfig({
                                  ...config,
                                  poller: { ...config.poller, zones: newZones },
                                });

                                const newEditing = { ...editingZones };
                                delete newEditing[idx];
                                setEditingZones(newEditing);

                                const newExpanded = { ...expandedZones };
                                delete newExpanded[idx];
                                setExpandedZones(newExpanded);
                              }}
                            >
                              <FiTrash2 />
                            </button>
                          </div>

                          {/* Expand button */}
                          <button
                            className="text-primary hover:text-hover-bg"
                            onClick={() =>
                              setExpandedZones({
                                ...expandedZones,
                                [idx]: !expanded,
                              })
                            }
                          >
                            {expanded ? <FiChevronUp /> : <FiChevronDown />}
                          </button>
                        </div>
                      </div>

                      {/* Expanded content */}
                      {expanded && (
                        <>
                          {editing ? (
                            <div className="space-y-2">
                              {zone.hostnames.map(
                                (host: string, hIdx: number) => (
                                  <div
                                    key={hIdx}
                                    className="flex items-center space-x-2"
                                  >
                                    <input
                                      className="border p-1 rounded flex-1"
                                      value={host}
                                      onChange={(e) => {
                                        const newZones = [
                                          ...config.poller.zones,
                                        ];
                                        newZones[idx].hostnames[hIdx] =
                                          e.target.value;
                                        setConfig({
                                          ...config,
                                          poller: {
                                            ...config.poller,
                                            zones: newZones,
                                          },
                                        });
                                      }}
                                    />
                                    <button
                                      onClick={() => {
                                        const newZones = [
                                          ...config.poller.zones,
                                        ];
                                        newZones[idx].hostnames.splice(hIdx, 1);
                                        setConfig({
                                          ...config,
                                          poller: {
                                            ...config.poller,
                                            zones: newZones,
                                          },
                                        });
                                      }}
                                    >
                                      <FiMinus />
                                    </button>
                                  </div>
                                )
                              )}
                              <button
                                className="px-2 py-1 border border-primary rounded"
                                onClick={() => {
                                  const newZones = [...config.poller.zones];
                                  newZones[idx].hostnames.push("");
                                  setConfig({
                                    ...config,
                                    poller: {
                                      ...config.poller,
                                      zones: newZones,
                                    },
                                  });
                                }}
                              >
                                + Add Device
                              </button>
                            </div>
                          ) : (
                            <div className="space-y-1">
                              {zone.hostnames.length > 0 ? (
                                zone.hostnames.map((h: string, i: number) => (
                                  <div
                                    key={i}
                                    className="border-b border-gray-300 last:border-b-0 pb-1"
                                  >
                                    {h}
                                  </div>
                                ))
                              ) : (
                                <div className="border-b border-gray-300 py-1">
                                  No devices
                                </div>
                              )}
                            </div>
                          )}
                        </>
                      )}

                      {/* Collapsed summary */}
                      {!expanded && !editing && (
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
                {draftZone === null ? (
                  <button
                    className="px-3 py-1 border border-primary rounded"
                    onClick={() => setDraftZone("")}
                  >
                    + Add Zone
                  </button>
                ) : (
                  <div className="flex items-center space-x-2">
                    <input
                      className="border p-1 rounded flex-1"
                      placeholder="Zone name"
                      value={draftZone}
                      onChange={(e) => setDraftZone(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault(); // prevent form submission or page reload
                          if (!draftZone) return;
                          setConfig({
                            ...config,
                            poller: {
                              ...config.poller,
                              zones: [
                                ...(config.poller.zones || []),
                                { zone: draftZone, hostnames: [] },
                              ],
                            },
                          });
                          setDraftZone(null);
                        }
                      }}
                    />

                    <button
                      className="px-2 py-1 border border-primary rounded"
                      onClick={() => {
                        if (!draftZone) return;
                        setConfig({
                          ...config,
                          poller: {
                            ...config.poller,
                            zones: [
                              ...(config.poller.zones || []),
                              { zone: draftZone, hostnames: [] },
                            ],
                          },
                        });
                        setDraftZone(null);
                      }}
                    >
                      Add
                    </button>
                    <button
                      className="px-2 py-1 border rounded"
                      onClick={() => setDraftZone(null)}
                    >
                      Cancel
                    </button>
                  </div>
                )}
              </div>
            )}

            {activeTab === "snmp" && (
              <div className="space-y-4">
                {config.poller?.snmp_groups?.map((grp: any, idx: number) => (
                  <div
                    key={idx}
                    className="space-y-1 rounded py-3 px-2 relative"
                  >
                    {/* Edit/Delete buttons */}
                    <div className="absolute top-2 right-2 flex space-x-2">
                      <button
                        className={`p-1 rounded transition ${
                          editIdx === idx
                            ? "bg-purple-500 text-white hover:bg-purple-600"
                            : "text-primary hover:text-hover-bg"
                        }`}
                        onClick={() => {
                          if (editIdx === idx) {
                            // Save action when clicking the check
                            setEditIdx(null);
                            // optionally do other save logic here
                          } else {
                            // Enter edit mode
                            setEditIdx(idx);
                          }
                        }}
                      >
                        {editIdx === idx ? <FiCheck /> : <FiEdit2 />}
                      </button>

                      <button
                        className="text-primary hover:text-hover-bg"
                        onClick={() => {
                          const newGroups = [...config.poller.snmp_groups];
                          newGroups.splice(idx, 1);
                          setConfig({
                            ...config,
                            poller: {
                              ...config.poller,
                              snmp_groups: newGroups,
                            },
                          });
                          if (editIdx === idx) setEditIdx(null); // reset edit mode if deleting
                        }}
                      >
                        <FiTrash2 />
                      </button>
                    </div>

                    <input
                      className="w-full border p-2 rounded mt-6"
                      value={grp.group_name}
                      placeholder="Group Name"
                      readOnly={editIdx !== idx} // only editable if this group is being edited
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
                      readOnly={editIdx !== idx} // only editable in edit mode
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
                        disabled={editIdx !== idx} // only editable in edit mode
                        onChange={(e) => {
                          const newGroups = [...config.poller.snmp_groups];
                          newGroups[idx].enabled = e.target.checked;
                          setConfig({
                            ...config,
                            poller: {
                              ...config.poller,
                              snmp_groups: newGroups,
                            },
                          });
                        }}
                      />
                      <span>Enabled</span>
                    </label>
                  </div>
                ))}

                <button
                  className="px-3 py-1 border border-primary rounded"
                  onClick={() => {
                    const groups = config.poller?.snmp_groups || [];
                    const lastGroup = groups[groups.length - 1];

                    // Only add if last group exists and has a name or IP
                    if (
                      !lastGroup ||
                      (lastGroup.group_name?.trim() &&
                        lastGroup.snmp_ip?.trim())
                    ) {
                      setConfig({
                        ...config,
                        poller: {
                          ...config.poller,
                          snmp_groups: [
                            ...groups,
                            { group_name: "", snmp_ip: "", enabled: true },
                          ],
                        },
                      });
                    }
                  }}
                >
                  + Add SNMP Group
                </button>
              </div>
            )}

            {activeTab === "advanced" && (
              <div className="space-y-4">
                {sections.map((section) => (
                  <details
                    key={section}
                    className="border rounded p-4"
                    open={expandedSections[section] ?? false}
                  >
                    <summary className="cursor-pointer flex justify-between items-center font-semibold">
                      <span>
                        {section.charAt(0).toUpperCase() + section.slice(1)}
                      </span>
                      <div className="flex gap-1">
                        <button
                          className={`p-1 rounded transition ${
                            editSection === section
                              ? "bg-purple-500 text-white hover:bg-purple-600"
                              : "text-primary hover:text-hover-bg"
                          }`}
                          onClick={(e) => {
                            e.preventDefault(); // prevent toggling details
                            setEditSection(
                              editSection === section ? null : section
                            );
                            setExpandedSections({
                              ...expandedSections,
                              [section]: !expandedSections[section],
                            });
                          }}
                        >
                          {editSection === section ? <FiCheck /> : <FiEdit2 />}
                        </button>
                        {/* Expand button */}
                        <button
                          type="button"
                          onClick={(e) => {
                            e.preventDefault(); // prevent toggling by default summary click
                            setExpandedSections({
                              ...expandedSections,
                              [section]: !expandedSections[section],
                            });
                          }}
                        >
                          {expandedSections[section] ? (
                            <FiChevronUp />
                          ) : (
                            <FiChevronDown />
                          )}
                        </button>
                      </div>
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
                            readOnly={
                              editSection !== section ||
                              (key.toLowerCase().includes("pass") &&
                                !authPasswordEdit)
                            }
                            onClick={() => {
                              if (
                                key.toLowerCase().includes("pass") &&
                                editSection === section && // <-- only when editing
                                !authPasswordEdit
                              ) {
                                const auth = prompt(
                                  "Enter admin password to edit:"
                                );
                                if (auth === "your-secret")
                                  setAuthPasswordEdit(true);
                              }
                            }}
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

            <div className="flex justify-end items-center gap-3 mt-6">
              {saving && <span className="text-sm text-gray-500">Saving…</span>}
              {!saving && saved && <span className="text-sm">Saved!</span>}
              <button
                onClick={handleSave}
                disabled={saving}
                className={`px-5 py-2 font-medium rounded-lg shadow transition
      ${
        saving
          ? "bg-hover-bg text-white cursor-not-allowed"
          : "bg-primary hover:bg-hover-bg text-white"
      }`}
              >
                Save
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
