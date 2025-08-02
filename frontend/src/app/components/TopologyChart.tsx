"use client";

import { DeviceNode } from "@/app/types/graphql/GetZoneDevices";
import React, { useState, useEffect, useRef, useMemo } from "react";
import {
  Network,
  DataSet,
  Node,
  Edge,
  Options,
} from "vis-network/standalone/esm/vis-network";
import { useTheme } from "next-themes";
import { formatUptime } from "@/app/utils/time";
import { useRouter } from "next/navigation";
/**
 * Renders a network topology chart using vis-network based on the given devices.
 *
 * @param {TopologyChartProps} props - The properties for the topology chart.
 * @param {Device[]} props.devices - Array of device objects representing nodes.
 * @param {boolean} props.loading - Loading state flag.
 * @param {Error | null} props.error - Error state, if any.
 *
 * @returns {JSX.Element} A React component rendering the network graph visualization.
 */

interface TopologyChartProps {
  devices: DeviceNode[];
  loading: boolean;
  error: string | null;
  zoomView?: boolean;
  clickToUse?: boolean;
}

export function TopologyChart({
  devices,
  loading,
  error,
  zoomView,
  clickToUse,
}: TopologyChartProps) {
  // React state to hold current graph structure: array of nodes and edges
  const [graph, setGraph] = useState<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });
  const router = useRouter();
  // State to track the current search input (used for node filtering/highlighting)
  const [inputTerm, setInputTerm] = useState("");
  // State to hold the search term for highlighting nodes
  const [searchTerm, setSearchTerm] = useState("");
  // State to track the search result
  const [searchResult, setSearchResult] = useState("");

  // Reference to the DOM element where the network will be rendered
  const containerRef = useRef<HTMLDivElement | null>(null);
  // Reference to the actual vis-network instance (used for calling methods like focus, fit, etc.)
  const networkRef = useRef<Network | null>(null);
  // DataSets are vis-network's internal reactive data structures for nodes and edges
  // These allow to dynamically add, update, or remove nodes/edges without recreating the network
  const nodesData = useRef<DataSet<Node> | null>(null);
  const edgesData = useRef<DataSet<Edge> | null>(null);
  // Theme context to determine if dark mode is enabled
  const { theme } = useTheme();
  // Stores the original, unmodified graph (used for resets, filtering, etc.)
  const initialGraph = React.useRef<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const [allNodeLabels, setAllNodeLabels] = useState<string[]>([]);

  // Determine if current theme is dark to set graph colors accordingly.
  // Note: vis-network options are initialized once and do not auto-update on theme change.
  // To support dynamic theme switching, update network options manually when `theme` changes.
  const isDark = theme === "dark";
  const options: Options = useMemo(
    () => ({
      clickToUse: clickToUse ?? true, // Use passed clickToUse prop or default to true
      layout: { hierarchical: false },
      physics: {
        enabled: true,
        solver: "barnesHut",
        stabilization: { iterations: 100, updateInterval: 25 },
      },
      edges: {
        color: isDark ? "#888" : "#BBB",
        width: 1,
        arrows: {
          to: {
            enabled: false, // Disable arrows by default
          },
        },
      },
      nodes: {
        shape: "dot",
        size: 15,
        color: isDark ? "#4A90E2" : "#1E90FF",
        font: {
          size: 12,
          color: isDark ? "#fff" : "black",
          strokeColor: isDark ? "#081028" : "white",
          strokeWidth: 2,
        },
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        dragNodes: true,
        zoomView: zoomView ?? true, // Use passed interaction options or default to true
        selectConnectedEdges: false,
      },
    }),
    [isDark]
  );

  useEffect(() => {
    /**
     * When the `devices` array updates, this effect builds the graph structure
     * (nodes and edges) to render a topology network using vis-network.
     *
     * - Each device becomes a node.
     * - If a device has interfaces with a CDP (Cisco Discovery Protocol) or
     *   LLDP(Link Layer Discovery Protocol) relationship,
     *   those relationships become edges.
     *
     * Custom `title` (tooltip) and `idxDevice` are added to nodes for UX features
     * like tooltips and click navigation.
     */
    // If no devices are available, reset the graph to empty state
    if (!devices || devices.length === 0) {
      setGraph({ nodes: [], edges: [] });
      return;
    }
    // Create sets to track unique nodes and edges
    // `nodesSet` tracks nodes already in the graph
    // `extraNodesSet` tracks nodes that are not in the current zone
    // This helps avoid duplicates and manage relationships correctly
    const nodesSet = new Set<string>();
    const extraNodesSet = new Set<string>();
    const edgesArray: Edge[] = [];
    // Iterate over each device to build nodes and edges
    // We use `sysName` as the unique identifier for each device
    devices.forEach((device) => {
      const sysName = device?.sysName;
      if (!sysName) return;
      // If the device is already in the current zone, remove it from `extraNodesSet`
      // This ensures we only add devices that are not in the current zone to `extraNodesSet`
      if (extraNodesSet.has(sysName)) {
        extraNodesSet.delete(sysName);
      }
      nodesSet.add(device.sysName);

      (device.l1interfaces?.edges ?? []).forEach(
        ({ node: iface }: { node: any }) => {
          const targetCDP = iface?.cdpcachedeviceid;
          const portCDP = iface?.cdpcachedeviceport;
          const targetLLDP = iface?.lldpcachedeviceid;
          const portLLDP = iface?.lldpcachedeviceport;
          // Create edges for CDP or LLDP relationships
          if (targetCDP) {
            if (!nodesSet.has(targetCDP)) {
              extraNodesSet.add(targetCDP);
            }
            edgesArray.push({
              from: sysName,
              to: targetCDP,
              label: "",
              title: portCDP,
              color: "#BBBBBB",
            } as Edge);
          } else if (targetLLDP) {
            if (!nodesSet.has(targetLLDP)) {
              extraNodesSet.add(targetLLDP);
            }
            edgesArray.push({
              from: sysName,
              to: targetLLDP,
              label: "",
              title: portLLDP,
              color: "#BBBBBB",
            } as Edge);
          }
        }
      );
    });
    function htmlTitle(html: string): HTMLElement {
      const container = document.createElement("div");
      container.innerHTML = html;
      return container;
    }

    // Create nodes array from devices
    // Each node has an `id`, `label`, `color`, and custom `title
    const nodesArray: Node[] = devices.map((device) => ({
      id: device.sysName ?? "",
      label: device.sysName ?? device.idxDevice?.toString() ?? "",
      color: "#1E90FF",
      idxDevice: device.idxDevice?.toString(), // custom field for navigation
      title: htmlTitle(
        `
    <div style="display: flex; align-items: flex-start; gap: 1rem;">
      <div>
        ${device.sysName ?? "Unknown"}<br>
        Hostname: ${device.hostname ?? "N/A"}
      </div>
      <div style="font-size: 2em;">
        ${
          typeof device.sysUptime === "number" && device.sysUptime > 0
            ? "🟢"
            : "🔴"
        }
      </div>
    </div>
    <div style="margin-top: 0.5rem; font-size: 1.2em; font-weight: bold; color: white;">
      ${formatUptime(device.sysUptime) ?? "N/A"}
      <span style="font-size: 0.4em; font-weight: normal;">Uptime</span>
    </div>
  `.trim()
      ),
    }));
    // Add extra nodes that are not in the current zone
    // These nodes are added with a different color and a tooltip
    // indicating they are not in the current zone
    extraNodesSet.forEach((sysName) => {
      nodesArray.push({
        id: sysName,
        label: sysName,
        color: "#383e44ff",
      });
    });
    // Clean up DOM elements in node titles
    initialGraph.current?.nodes?.forEach((node) => {
      if (
        node.title instanceof HTMLElement &&
        typeof node.title.remove === "function"
      ) {
        node.title.remove();
      }
    });
    // Clean up DOM elements in edge titles
    initialGraph.current?.edges?.forEach((edge) => {
      if (
        edge.title instanceof HTMLElement &&
        typeof edge.title.remove === "function"
      ) {
        edge.title.remove();
      }
    });

    // Set the new graph
    initialGraph.current = { nodes: nodesArray, edges: edgesArray };
    setGraph({ nodes: nodesArray, edges: edgesArray });

    if (networkRef.current) {
      networkRef.current.fit();
      networkRef.current.moveTo({
        position: { x: 0, y: 0 },
        scale: 1,
        animation: true,
      });
    }
  }, [devices]);

  useEffect(() => {
    // If no graph data is available, do not render the network
    if (!containerRef.current || graph.nodes.length === 0) return;
    nodesData.current = new DataSet<Node>(graph.nodes);
    edgesData.current = new DataSet<Edge>(graph.edges);
    networkRef.current = new Network(
      containerRef.current,
      {
        nodes: nodesData.current,
        edges: edgesData.current,
      },
      options
    );

    // Double-click event to navigate to device details
    // When a node is double-clicked, it navigates to the device details page
    networkRef.current.on("doubleClick", (params) => {
      if (params.nodes.length === 1) {
        const nodeId = params.nodes[0];
        const nodeData = nodesData.current?.get(nodeId);
        const node = Array.isArray(nodeData) ? nodeData[0] : nodeData;
        const idxDevice = (node as any)?.idxDevice ?? nodeId;
        const sysName = (node as any)?.label ?? "";
        const url = `/devices/${encodeURIComponent(
          idxDevice
        )}?sysName=${encodeURIComponent(sysName)}#devices-overview`;
        router.push(url);
      }
    });

    // Node selection highlighting
    // When a node is selected, it highlights the node and dims others
    // It also updates the edges to have a different color

    networkRef.current.on("selectNode", ({ nodes }) => {
      const selected = nodes[0];
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        const isSelected = node.id === selected;
        nodesData.current!.update({
          id: node.id,
          opacity: isSelected ? 1 : 0.6,
          color: {
            border: isDark ? "#999" : "#555",
          },
          font: {
            color: isSelected
              ? isDark
                ? "#fff"
                : "black"
              : isDark
              ? "#aaa"
              : "#A9A9A9",
          },
        });
      });
    });
    // Reset node selection highlighting
    // When a node is deselected, it resets the opacity and color of all nodes
    // It also resets the edges color to default
    networkRef.current.on("deselectNode", () => {
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        nodesData.current!.update({
          id: node.id,
          opacity: 1,
          color: {
            border: isDark ? "#999" : "#555",
          },
          font: {
            color: isDark ? "#fff" : "black",
          },
        });
      });
      // Reset edges color
      initialGraph.current.edges.forEach((originalEdge) => {
        edgesData.current!.update({
          id: originalEdge.id,
          color: originalEdge.color || (isDark ? "#444" : "#BBBBBB"), // fallback if color missing
        });
      });
    });
    // Show arrow on hover
    networkRef.current.on("hoverEdge", (params) => {
      if (!edgesData.current) return;

      edgesData.current.update({
        id: params.edge,
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      });
    });

    networkRef.current.on("blurEdge", (params) => {
      if (!edgesData.current || !networkRef.current) return;

      const selectedEdges = networkRef.current.getSelectedEdges();

      if (!selectedEdges.includes(params.edge)) {
        edgesData.current.update({
          id: params.edge,
          arrows: { to: false },
        });
      }
    });

    networkRef.current.on("selectEdge", (params) => {
      if (!edgesData.current) return;

      edgesData.current.update({
        id: params.edges[0], // handles single selection
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      });
    });

    networkRef.current.on("deselectEdge", (params) => {
      if (!edgesData.current) return;

      initialGraph.current.edges.forEach((originalEdge) => {
        edgesData.current!.update({
          id: originalEdge.id,
          color: originalEdge.color || (isDark ? "#444" : "#BBBBBB"), // fallback if color missing
          arrows: { to: false }, // reset arrow visibility
        });
      });
    });
    const labels =
      nodesData.current
        ?.get()
        ?.map((node: any) => node.label)
        .filter(Boolean) || [];

    setAllNodeLabels(labels);
  }, [graph, theme]);

  useEffect(() => {
    if (!inputTerm || inputTerm.trim() === "") {
      setSuggestions([]);
      return;
    }

    const filtered = allNodeLabels
      .filter((label) => label.toLowerCase().includes(inputTerm.toLowerCase()))
      .slice(0, 5); // limit to top 5

    setSuggestions(filtered);
  }, [inputTerm, allNodeLabels]);

  // Effect to handle search term changes
  // When the search term changes, it highlights the matching node and focuses the network view on it.
  // If the node is not found, it logs a warning.
  useEffect(() => {
    if (!searchTerm || !nodesData.current || !networkRef.current) return;

    const node = nodesData.current.get(searchTerm);
    if (!node) {
      setSearchResult("No results found for: " + searchTerm);
      return;
    } else {
      // Highlight the node and focus the network
      setSearchResult("Showing results for: " + searchTerm);

      networkRef.current.focus(searchTerm, { scale: 1.5, animation: true });

      nodesData.current.get().forEach((n) => {
        nodesData.current!.update({
          id: n.id,
          color: {
            background: n.id === searchTerm ? "#FF6347" : "#D3D3D3",
            border: "#555",
          },
          font: {
            color:
              n.id === searchTerm
                ? isDark
                  ? "#fff"
                  : "black"
                : isDark
                ? "#aaa"
                : "#A9A9A9",
          },
        });
      });
    }
  }, [searchTerm]);

  const handleReset = () => {
    setInputTerm("");
    setSearchResult("");
    setGraph(initialGraph.current);

    if (!networkRef.current || !nodesData.current || !edgesData.current) return;

    // Clear selection
    networkRef.current.unselectAll();

    // Instead of clear + add, do update
    const originalNodes = initialGraph.current.nodes;
    const originalEdges = initialGraph.current.edges;

    nodesData.current.clear();
    edgesData.current.clear();

    nodesData.current.add(originalNodes);
    edgesData.current.add(originalEdges);

    // Reset view
    networkRef.current.fit();
  };

  const handleExportImage = () => {
    const canvas = containerRef.current?.getElementsByTagName("canvas")[0];
    if (!canvas) return;

    const image = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.href = image;
    link.download = "topology.png";
    link.click();
  };

  if (loading) return <p>Loading topology...</p>;
  if (error) return <p>Error loading topology: {error}</p>;

  return (
    <div className="topology-chart-container">
      <h2 className="text-xl font-semibold mb-2 topology-title">
        Network Topology
      </h2>
      <div className="flex mb-2 w-full gap-4 flex-wrap justify-between topology-controls">
        <div className="relative max-w-sm flex-grow topology-search-container">
          <form
            className="flex items-center gap-4 topology-search-form"
            onSubmit={(e) => {
              e.preventDefault();
              setSearchTerm(inputTerm);
              setInputTerm("");
            }}
          >
            <input
              className="border p-2 rounded w-full topology-search-input"
              type="text"
              placeholder="Search device..."
              value={inputTerm}
              onChange={(e) => {
                const value = e.target.value;
                setInputTerm(value);
                if (value.trim() === "") {
                  setSuggestions([]);
                  return;
                }
                const filtered = allNodeLabels
                  .filter((label) =>
                    label.toLowerCase().includes(value.toLowerCase())
                  )
                  .slice(0, 5);
                setSuggestions(filtered);
              }}
            />
            <button className="border-2 text-button rounded px-4 py-2 cursor-pointer transition-colors duration-300 align-middle h-fit topology-search-btn">
              Search
            </button>
          </form>

          {suggestions.length > 0 && (
            <ul className="absolute bg-bg shadow-md mt-1 rounded border w-full z-50 topology-suggestions-list">
              {suggestions.map((suggestion, index) => (
                <li
                  key={index}
                  onClick={() => {
                    setSearchTerm(suggestion);
                    setInputTerm("");
                    setSuggestions([]);
                  }}
                  className="cursor-pointer px-4 py-2 hover:bg-hover-bg topology-suggestion-item"
                >
                  {suggestion}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="flex items-center gap-4 topology-action-buttons">
          <button
            onClick={handleReset}
            className="reset-button topology-reset-btn"
          >
            Reset
          </button>
          <button
            onClick={handleExportImage}
            className="text-white rounded px-4 py-2 cursor-pointer transition-colors duration-300 topology-export-btn"
            style={{ backgroundColor: "#CB3CFF" }}
          >
            Export
          </button>
        </div>
      </div>

      <p className="mt-2 mb-2 text-sm text-gray-600 h-fit topology-search-result">
        {searchResult || ""}
      </p>

      <div
        ref={containerRef}
        className="w-full h-[70vh] border rounded topology-network-canvas"
      />
      <div
        className="topology-instructions"
        style={{ margin: "0.25rem", fontSize: "0.85rem", color: "#666" }}
      >
        Single-click to select nodes, double-click to open device details.
      </div>
    </div>
  );
}
