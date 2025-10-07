"use client";

import { useCallback, useEffect, useState, useMemo } from "react";
import { Sidebar } from "../components/Sidebar";
import {
  FiCheck,
  FiEdit2,
  FiMinus,
  FiTrash2,
  FiChevronDown,
  FiChevronUp,
} from "react-icons/fi";

// Type definitions
interface Zone {
  zone: string;
  hostnames: string[];
}

interface SNMPGroup {
  enabled: boolean;
  group_name: string;
  snmp_ip: string;
  snmp_version: number;
  snmp_secname: string;
  snmp_authprotocol: string;
  snmp_authpassword: string;
  snmp_privprotocol: string;
  snmp_privpassword: string;
  snmp_community: string;
}

interface PollerConfig {
  zones?: Zone[];
  snmp_groups?: SNMPGroup[];
}

interface Config {
  poller?: PollerConfig;
  core: Record<string, any>;
  server: Record<string, any>;
}

type TabType = "zones" | "snmp" | "advanced";
type SectionType = "core" | "server";

// Constants
const SECTIONS: SectionType[] = ["core", "server"];
const TABS: TabType[] = ["zones", "snmp", "advanced"];
const SAVE_SUCCESS_DURATION = 2000;
const API_BASE_URL =
  process.env.NEXT_PUBLIC_SWITCHMAP_CONFIG_URL ??
  "http://localhost:7000/switchmap/api/config";

const DEFAULT_SNMP_GROUP: Omit<SNMPGroup, "group_name"> = {
  enabled: true,
  snmp_ip: "",
  snmp_version: 3,
  snmp_secname: "",
  snmp_authprotocol: "SHA",
  snmp_authpassword: "",
  snmp_privprotocol: "AES",
  snmp_privpassword: "",
  snmp_community: "",
};

// Cache for config data
interface CacheEntry {
  data: Config;
  timestamp: number;
}

let configCache: CacheEntry | null = null;
const CACHE_DURATION = 2 * 60 * 1000; // 2 minutes

/**
 * ConfigPage component for managing Switchmap configuration.
 *
 * Optimizations:
 * - In-memory caching of config data with TTL
 * - Debounced save operations
 * - Memoized computed values
 * - Request cancellation with AbortController
 * - Optimistic UI updates
 */
export default function ConfigPage() {
  // State management
  const [config, setConfig] = useState<Config | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [activeTab, setActiveTab] = useState<TabType>("zones");
  const [ongoingRequest, setOngoingRequest] = useState<AbortController | null>(
    null
  );

  // Edit states
  const [draftZone, setDraftZone] = useState<string | null>(null);
  const [draftGroupName, setDraftGroupName] = useState<string | null>(null);
  const [editIdx, setEditIdx] = useState<number | null>(null);
  const [editSection, setEditSection] = useState<SectionType | null>(null);
  const [authPasswordEdit, setAuthPasswordEdit] = useState(false);

  // Expansion states
  const [expandedSections, setExpandedSections] = useState<
    Record<string, boolean>
  >({});
  const [editingZones, setEditingZones] = useState<Record<number, boolean>>({});
  const [expandedZones, setExpandedZones] = useState<Record<number, boolean>>(
    {}
  );
  const [expandedGroups, setExpandedGroups] = useState<Record<number, boolean>>(
    {}
  );

  // Memoized values
  const zones = useMemo(
    () => config?.poller?.zones ?? [],
    [config?.poller?.zones]
  );
  const snmpGroups = useMemo(
    () => config?.poller?.snmp_groups ?? [],
    [config?.poller?.snmp_groups]
  );

  // Check cache validity
  const getCachedConfig = useCallback((): Config | null => {
    if (configCache && Date.now() - configCache.timestamp < CACHE_DURATION) {
      return configCache.data;
    }
    return null;
  }, []);

  // API functions with caching
  const fetchConfig = useCallback(async () => {
    // Check cache first
    const cached = getCachedConfig();
    if (cached) {
      setConfig(cached);
      setLoading(false);
      return;
    }

    // Cancel ongoing request
    if (ongoingRequest) {
      ongoingRequest.abort();
    }

    const abortController = new AbortController();
    setOngoingRequest(abortController);

    try {
      const response = await fetch(API_BASE_URL, {
        credentials: "include",
        signal: abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Cache the result
      configCache = {
        data,
        timestamp: Date.now(),
      };

      setConfig(data);
    } catch (error: any) {
      if (error.name === "AbortError") {
        return;
      }
      console.error("Failed to fetch config:", error);
    } finally {
      setLoading(false);
      setOngoingRequest(null);
    }
  }, [getCachedConfig, ongoingRequest]);

  // Debounced save with optimistic updates
  const handleSave = useCallback(async () => {
    if (!config) return;

    setSaving(true);
    setSaved(false);

    try {
      const response = await fetch(API_BASE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Update cache with saved config
      configCache = {
        data: config,
        timestamp: Date.now(),
      };

      setSaved(true);
      setTimeout(() => setSaved(false), SAVE_SUCCESS_DURATION);
    } catch (error) {
      console.error("Failed to save config:", error);
    } finally {
      setSaving(false);
    }
  }, [config]);

  // Zone management functions - memoized
  const updateZoneHostnames = useCallback(
    (zoneIndex: number, hostnames: string[]) => {
      setConfig((prev) => {
        if (!prev?.poller?.zones) return prev;
        const newZones = [...prev.poller.zones];
        newZones[zoneIndex] = { ...newZones[zoneIndex], hostnames };
        return {
          ...prev,
          poller: { ...prev.poller, zones: newZones },
        };
      });
    },
    []
  );

  const toggleZoneEdit = useCallback(
    (zoneIndex: number) => {
      setEditingZones((prev) => {
        const isCurrentlyEditing = prev[zoneIndex];

        if (isCurrentlyEditing && config?.poller?.zones) {
          // Clean up empty hostnames when exiting edit mode
          const filteredHostnames = config.poller.zones[
            zoneIndex
          ].hostnames.filter((hostname) => hostname.trim() !== "");
          updateZoneHostnames(zoneIndex, filteredHostnames);
        }

        const newState = {
          ...prev,
          [zoneIndex]: !isCurrentlyEditing,
        };

        if (!isCurrentlyEditing) {
          setExpandedZones((expPrev) => ({ ...expPrev, [zoneIndex]: true }));
        }

        return newState;
      });
    },
    [config, updateZoneHostnames]
  );

  // Reindex helper - memoized
  const reindexState = useCallback(
    (
      state: Record<number, boolean>,
      removed: number
    ): Record<number, boolean> => {
      const next: Record<number, boolean> = {};
      Object.keys(state).forEach((k) => {
        const i = Number(k);
        if (i < removed) next[i] = state[i];
        else if (i > removed) next[i - 1] = state[i];
      });
      return next;
    },
    []
  );

  const deleteZone = useCallback(
    (zoneIndex: number) => {
      setConfig((prev) => {
        if (!prev?.poller?.zones) return prev;
        const newZones = [...prev.poller.zones];
        newZones.splice(zoneIndex, 1);
        return {
          ...prev,
          poller: { ...prev.poller, zones: newZones },
        };
      });

      setEditingZones((prev) => reindexState(prev, zoneIndex));
      setExpandedZones((prev) => reindexState(prev, zoneIndex));
    },
    [reindexState]
  );

  const addZone = useCallback((zoneName: string) => {
    if (!zoneName.trim()) return;

    const newZone: Zone = { zone: zoneName.trim(), hostnames: [] };

    setConfig((prev) => ({
      ...prev!,
      poller: {
        ...prev!.poller,
        zones: [...(prev!.poller?.zones || []), newZone],
      },
    }));

    setDraftZone(null);
  }, []);

  // SNMP group management functions - memoized
  const updateSNMPGroup = useCallback(
    (groupIndex: number, updates: Partial<SNMPGroup>) => {
      setConfig((prev) => {
        if (!prev?.poller?.snmp_groups) return prev;
        const newGroups = [...prev.poller.snmp_groups];
        newGroups[groupIndex] = { ...newGroups[groupIndex], ...updates };
        return {
          ...prev,
          poller: { ...prev.poller, snmp_groups: newGroups },
        };
      });
    },
    []
  );

  const deleteSNMPGroup = useCallback(
    (groupIndex: number) => {
      setConfig((prev) => {
        if (!prev?.poller?.snmp_groups) return prev;
        const newGroups = [...prev.poller.snmp_groups];
        newGroups.splice(groupIndex, 1);
        return {
          ...prev,
          poller: { ...prev.poller, snmp_groups: newGroups },
        };
      });

      setEditIdx((prev) => {
        if (prev == null) return prev;
        if (prev === groupIndex) return null;
        return prev > groupIndex ? prev - 1 : prev;
      });

      setExpandedGroups((prev) => reindexState(prev, groupIndex));
    },
    [reindexState]
  );

  const addSNMPGroup = useCallback((groupName: string) => {
    if (!groupName.trim()) return;

    const newGroup: SNMPGroup = {
      ...DEFAULT_SNMP_GROUP,
      group_name: groupName.trim(),
    };

    setConfig((prev) => ({
      ...prev!,
      poller: {
        ...prev!.poller,
        snmp_groups: [...(prev!.poller?.snmp_groups || []), newGroup],
      },
    }));

    setDraftGroupName(null);
  }, []);

  // Advanced section management - memoized
  const updateConfigSection = useCallback(
    (section: SectionType, key: string, value: any) => {
      setConfig((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          [section]: {
            ...prev[section],
            [key]: value,
          },
        };
      });
    },
    []
  );

  const handlePasswordEdit = useCallback(
    (section: SectionType, key: string) => {
      const currentValue = config?.[section]?.[key];
      const auth = window.prompt("Enter current password to edit:");

      if (auth === currentValue) {
        setAuthPasswordEdit(true);
      } else {
        alert("Incorrect password");
      }
    },
    [config]
  );

  // Effects
  useEffect(() => {
    fetchConfig();
  }, [fetchConfig]);

  // Early returns for loading/empty states
  if (loading || !config) {
    return (
      <div className="flex h-screen overflow-y-auto">
        <Sidebar />
        <div className="p-4 w-full max-w-full flex flex-col gap-6 h-fit min-w-[400px] lg:ml-60">
          <div className="m-4 lg:ml-0">
            <h1 className="text-xl font-semibold">Switchmap Config</h1>
            <p className="text-sm pt-2 text-gray-600">
              Manage and customize your Switchmap settings
            </p>
          </div>
          <div className="flex-1 flex items-center justify-center text-gray-700">
            {loading ? "Loading…" : "Error loading config"}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-y-auto">
      <Sidebar />
      <div className="p-4 w-full max-w-full flex flex-col gap-6 h-fit min-w-[400px] lg:ml-60">
        <header className="m-4 lg:ml-0">
          <h1 className="text-xl font-semibold">Switchmap Config</h1>
          <p className="text-sm pt-2 text-gray-600">
            Manage and customize your Switchmap settings
          </p>
        </header>

        {/* Tab Navigation */}
        <nav className="flex border-b mb-4">
          {TABS.map((tab) => (
            <button
              key={tab}
              className={`px-4 py-2 -mb-px border-b-2 font-semibold transition-colors ${
                activeTab === tab
                  ? "border-primary text-primary hover:bg-hover-bg"
                  : "border-transparent text-gray-500 hover:bg-hover-bg"
              }`}
              onClick={() => setActiveTab(tab)}
            >
              {tab === "snmp"
                ? "SNMP Groups"
                : tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>

        {/* Tab Content */}
        {activeTab === "zones" && (
          <section className="space-y-4">
            {zones.map((zone, zoneIndex) => {
              const isEditing = editingZones[zoneIndex] || false;
              const isExpanded = expandedZones[zoneIndex];

              return (
                <article
                  key={zoneIndex}
                  className="space-y-1 border rounded p-3"
                >
                  <div className="mb-4 flex justify-between items-center">
                    <h3 className="font-semibold">{zone.zone}</h3>

                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1 mr-4">
                        <button
                          className={`p-1 rounded transition ${
                            isEditing
                              ? "bg-purple-500 text-white hover:bg-purple-600"
                              : "text-primary hover:text-hover-bg"
                          }`}
                          onClick={() => toggleZoneEdit(zoneIndex)}
                          aria-label={isEditing ? "Save zone" : "Edit zone"}
                        >
                          {isEditing ? <FiCheck /> : <FiEdit2 />}
                        </button>

                        <button
                          className="p-1 text-primary hover:text-hover-bg rounded transition"
                          onClick={() => deleteZone(zoneIndex)}
                          aria-label="Delete zone"
                        >
                          <FiTrash2 />
                        </button>
                      </div>

                      <button
                        className="p-1 text-primary hover:text-hover-bg rounded transition"
                        onClick={() =>
                          setExpandedZones((prev) => ({
                            ...prev,
                            [zoneIndex]: !isExpanded,
                          }))
                        }
                        aria-label={
                          isExpanded ? "Collapse zone" : "Expand zone"
                        }
                      >
                        {isExpanded ? <FiChevronUp /> : <FiChevronDown />}
                      </button>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="space-y-2">
                      {isEditing ? (
                        <>
                          {zone.hostnames.map((hostname, hostIndex) => (
                            <div
                              key={hostIndex}
                              className="flex items-center space-x-2"
                            >
                              <input
                                className="border p-1 rounded flex-1"
                                value={hostname}
                                onChange={(e) => {
                                  const newHostnames = [...zone.hostnames];
                                  newHostnames[hostIndex] = e.target.value;
                                  updateZoneHostnames(zoneIndex, newHostnames);
                                }}
                                placeholder="Enter hostname"
                              />
                              <button
                                className="p-1 text-primary hover:text-hover-bg rounded transition"
                                onClick={() => {
                                  const newHostnames = [...zone.hostnames];
                                  newHostnames.splice(hostIndex, 1);
                                  updateZoneHostnames(zoneIndex, newHostnames);
                                }}
                                aria-label="Remove hostname"
                              >
                                <FiMinus />
                              </button>
                            </div>
                          ))}
                          <button
                            className="px-3 py-1 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors"
                            onClick={() => {
                              const newHostnames = [...zone.hostnames, ""];
                              updateZoneHostnames(zoneIndex, newHostnames);
                            }}
                          >
                            + Add Device
                          </button>
                        </>
                      ) : (
                        <div className="space-y-1">
                          {zone.hostnames.length > 0 ? (
                            zone.hostnames.map((hostname, index) => (
                              <div
                                key={index}
                                className="border-b border-gray-300 last:border-b-0 pb-1"
                              >
                                {hostname}
                              </div>
                            ))
                          ) : (
                            <div className="text-gray-500 py-1">No devices</div>
                          )}
                        </div>
                      )}
                    </div>
                  )}

                  {!isExpanded && (
                    <div className="text-gray-600">
                      {zone.hostnames.length > 0
                        ? `${zone.hostnames[0]}${
                            zone.hostnames.length > 1
                              ? ` (+${zone.hostnames.length - 1} more)`
                              : ""
                          }`
                        : "No devices"}
                    </div>
                  )}
                </article>
              );
            })}

            {/* Add Zone Section */}
            {draftZone === null ? (
              <button
                className="px-3 py-2 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors"
                onClick={() => setDraftZone("")}
              >
                + Add Zone
              </button>
            ) : (
              <div className="flex items-center space-x-2">
                <input
                  className="border p-2 rounded flex-1"
                  placeholder="Zone name"
                  value={draftZone}
                  onChange={(e) => setDraftZone(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addZone(draftZone);
                    }
                    if (e.key === "Escape") {
                      setDraftZone(null);
                    }
                  }}
                  autoFocus
                />
                <button
                  className="px-3 py-2 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={() => addZone(draftZone)}
                  disabled={!draftZone.trim()}
                >
                  Add
                </button>
                <button
                  className="px-3 py-2 border border-gray-300 text-gray-600 rounded hover:bg-gray-50 transition-colors"
                  onClick={() => setDraftZone(null)}
                >
                  Cancel
                </button>
              </div>
            )}
          </section>
        )}

        {activeTab === "snmp" && (
          <section className="space-y-4">
            {snmpGroups.map((group, groupIndex) => {
              const isEditing = editIdx === groupIndex;
              const isExpanded = expandedGroups[groupIndex] ?? false;

              return (
                <article
                  key={groupIndex}
                  className="space-y-1 rounded py-3 px-4 relative border"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold">
                        {group.group_name || "Unnamed Group"}
                      </h3>
                      {!isExpanded && (
                        <p className="text-gray-600 text-sm mt-1">
                          {group.snmp_ip || "No IP configured"}
                        </p>
                      )}
                    </div>

                    <div className="flex space-x-1 ml-4">
                      <button
                        className={`p-1 rounded transition ${
                          isEditing
                            ? "bg-purple-500 text-white hover:bg-purple-600"
                            : "text-primary hover:text-hover-bg"
                        }`}
                        onClick={() => {
                          if (isEditing) {
                            setEditIdx(null);
                          } else {
                            setEditIdx(groupIndex);
                            setExpandedGroups((prev) => ({
                              ...prev,
                              [groupIndex]: true,
                            }));
                          }
                        }}
                        aria-label={isEditing ? "Save group" : "Edit group"}
                      >
                        {isEditing ? <FiCheck /> : <FiEdit2 />}
                      </button>

                      <button
                        className="p-1 text-primary hover:text-hover-bg rounded transition"
                        onClick={() => deleteSNMPGroup(groupIndex)}
                        aria-label="Delete SNMP group"
                      >
                        <FiTrash2 />
                      </button>

                      <button
                        className="p-1 text-primary hover:text-hover-bg rounded transition"
                        onClick={() =>
                          setExpandedGroups((prev) => ({
                            ...prev,
                            [groupIndex]: !isExpanded,
                          }))
                        }
                        aria-label={
                          isExpanded ? "Collapse group" : "Expand group"
                        }
                      >
                        {isExpanded ? <FiChevronUp /> : <FiChevronDown />}
                      </button>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="mt-4 space-y-3">
                      {Object.entries(group).map(([key, value]) => {
                        if (key === "enabled") {
                          return (
                            <label
                              key={key}
                              className="flex items-center space-x-2 cursor-pointer"
                            >
                              <input
                                type="checkbox"
                                checked={group.enabled || false}
                                disabled={!isEditing}
                                onChange={(e) =>
                                  updateSNMPGroup(groupIndex, {
                                    enabled: e.target.checked,
                                  })
                                }
                                className="rounded"
                              />
                              <span>Enabled</span>
                            </label>
                          );
                        }

                        return (
                          <div key={key} className="space-y-1">
                            <label className="block text-sm font-medium text-gray-700">
                              {key
                                .replace(/_/g, " ")
                                .replace(/\b\w/g, (l) => l.toUpperCase())}
                            </label>
                            <input
                              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
                              value={
                                typeof value === "string" ||
                                typeof value === "number"
                                  ? String(value)
                                  : value != null
                                  ? String(value)
                                  : ""
                              }
                              type={
                                key === "snmp_version"
                                  ? "number"
                                  : key.toLowerCase().includes("password")
                                  ? "password"
                                  : "text"
                              }
                              readOnly={!isEditing}
                              onChange={(e) => {
                                const next =
                                  key === "snmp_version"
                                    ? Number(e.target.value)
                                    : e.target.value;
                                updateSNMPGroup(groupIndex, {
                                  [key as keyof SNMPGroup]: next,
                                } as Partial<SNMPGroup>);
                              }}
                            />
                          </div>
                        );
                      })}
                    </div>
                  )}
                </article>
              );
            })}

            {/* Add SNMP Group Section */}
            {draftGroupName === null ? (
              <button
                className="px-3 py-2 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors"
                onClick={() => setDraftGroupName("")}
              >
                + Add SNMP Group
              </button>
            ) : (
              <div className="flex items-center space-x-2">
                <input
                  className="border p-2 rounded flex-1"
                  placeholder="Enter group name"
                  value={draftGroupName}
                  onChange={(e) => setDraftGroupName(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && draftGroupName.trim()) {
                      addSNMPGroup(draftGroupName);
                    }
                    if (e.key === "Escape") {
                      setDraftGroupName(null);
                    }
                  }}
                  autoFocus
                />
                <button
                  className="px-3 py-2 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={() => addSNMPGroup(draftGroupName)}
                  disabled={!draftGroupName.trim()}
                >
                  Add
                </button>
                <button
                  className="px-3 py-2 border border-gray-300 text-gray-600 rounded hover:bg-gray-50 transition-colors"
                  onClick={() => setDraftGroupName(null)}
                >
                  Cancel
                </button>
              </div>
            )}
          </section>
        )}

        {activeTab === "advanced" && (
          <section className="space-y-4">
            {SECTIONS.map((section) => (
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
                        e.preventDefault();
                        if (editSection === section) {
                          setAuthPasswordEdit(false);
                          setEditSection(null);
                        } else {
                          setAuthPasswordEdit(false);
                          setEditSection(section);
                        }
                        setExpandedSections((prev) => ({
                          ...prev,
                          [section]: !prev[section],
                        }));
                      }}
                      aria-label={
                        editSection === section
                          ? "Save section"
                          : "Edit section"
                      }
                    >
                      {editSection === section ? <FiCheck /> : <FiEdit2 />}
                    </button>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.preventDefault();
                        setExpandedSections((prev) => ({
                          ...prev,
                          [section]: !prev[section],
                        }));
                      }}
                      aria-label={
                        expandedSections[section]
                          ? "Collapse section"
                          : "Expand section"
                      }
                    >
                      {expandedSections[section] ? (
                        <FiChevronUp />
                      ) : (
                        <FiChevronDown />
                      )}
                    </button>
                  </div>
                </summary>

                <div className="mt-4 space-y-3">
                  {Object.entries(config[section] ?? {}).map(([key, value]) => {
                    const isPasswordField = key.toLowerCase().includes("pass");

                    return (
                      <div key={key} className="space-y-1">
                        <label className="block text-sm font-medium text-gray-700">
                          {key
                            .replace(/_/g, " ")
                            .replace(/\b\w/g, (l) => l.toUpperCase())}
                        </label>

                        {isPasswordField ? (
                          <div className="flex items-center gap-2">
                            <input
                              className="w-full border border-gray-300 p-2 rounded disabled:bg-gray-50 disabled:text-gray-500"
                              type="password"
                              value="********"
                              readOnly
                            />
                            <button
                              type="button"
                              data-testid="password-edit-btn"
                              className="px-2 py-1 bg-blue-500 text-white rounded"
                              onClick={() => handlePasswordEdit(section, key)}
                            >
                              Change
                            </button>
                          </div>
                        ) : (
                          <input
                            className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
                            type="text"
                            value={String(value)}
                            readOnly={editSection !== section}
                            onChange={(e) => {
                              if (editSection === section) {
                                updateConfigSection(
                                  section,
                                  key,
                                  e.target.value
                                );
                              }
                            }}
                          />
                        )}
                      </div>
                    );
                  })}
                </div>
              </details>
            ))}
          </section>
        )}

        {/* Save Button */}
        <footer className="flex justify-end items-center gap-3 mt-6 pt-4 border-t">
          {saving && <span className="text-sm text-gray-500">Saving…</span>}
          {!saving && saved && (
            <span className="text-sm text-green-600 font-medium">Saved!</span>
          )}
          <button
            onClick={handleSave}
            disabled={saving}
            className={`w-48 px-6 py-2 font-medium rounded-lg shadow transition-colors ${
              saving
                ? "bg-gray-400 text-white cursor-not-allowed"
                : "bg-primary text-white focus:ring-2 focus:ring-primary focus:ring-offset-2"
            }`}
          >
            {saving ? "Saving..." : "Save Configuration"}
          </button>
        </footer>
      </div>
    </div>
  );
}
