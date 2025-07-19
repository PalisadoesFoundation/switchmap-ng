"use client";

import { DeviceNode } from "@/types/graphql/GetZoneDevices";
import React, { useState, useEffect, useRef } from "react";
import {
  Network,
  DataSet,
  Node,
  Edge,
  Options,
} from "vis-network/standalone/esm/vis-network";
import { useTheme } from "next-themes";
import { formatUptime } from "@/utils/time";
import { truncateLines } from "@/utils/stringUtils";

interface TopologyChartProps {
  devices: DeviceNode[];
  loading: boolean;
  error: string | null;
}

export default function TopologyChart({
  devices,
  loading,
  error,
}: TopologyChartProps) {
  // React state to hold current graph structure: array of nodes and edges
  const [graph, setGraph] = useState<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });
  // State to track the current search input (used for node filtering/highlighting)
  const [searchTerm, setSearchTerm] = useState("");
  // Reference to the DOM element where the network will be rendered
  const containerRef = useRef<HTMLDivElement | null>(null);
  // Reference to the actual vis-network instance (used for calling methods like focus, fit, etc.)
  const networkRef = useRef<Network | null>(null);
  // DataSets are vis-network's internal reactive data structures for nodes and edges
  // These allow you to dynamically add, update, or remove nodes/edges without recreating the network
  const nodesData = useRef<DataSet<Node> | null>(null);
  const edgesData = useRef<DataSet<Edge> | null>(null);
  // Theme context to determine if dark mode is enabled
  const { theme } = useTheme();
  // Stores the original, unmodified graph (used for resets, filtering, etc.)
  const initialGraph = React.useRef<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });

  // Determine if current theme is dark to set graph colors accordingly.
  // Note: vis-network options are initialized once and do not auto-update on theme change.
  // To support dynamic theme switching, update network options manually when `theme` changes.
  const isDark = theme === "dark";
  const options: Options = {
    clickToUse: true,
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
      zoomView: true,
    },
  };

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
          const targetLLDP = iface?.cdpcachedeviceid;
          const portLLDP = iface?.cdpcachedeviceport;
          // Create edges for CDP or LLDP relationships
          if (targetCDP) {
            if (!nodesSet.has(targetCDP)) {
              extraNodesSet.add(targetCDP);
            }
            edgesArray.push({
              from: sysName,
              to: targetCDP,
              label: "",
              title: String("CDP " + (portCDP ?? "")),
              color: "#BBBBBB",
            } as Edge);
          }
          if (targetLLDP) {
            if (!nodesSet.has(targetLLDP)) {
              extraNodesSet.add(targetLLDP);
            }
            edgesArray.push({
              from: sysName,
              to: targetLLDP,
              label: "",
              title: String("LLDP " + (portLLDP ?? "")),
              color: "#6f6f6fff",
            } as Edge);
          }
        }
      );
    });

    // Create nodes array from devices
    // Each node has an `id`, `label`, `color`, and custom `title
    const nodesArray: Node[] = devices.map((device) => ({
      id: device.sysName ?? "",
      label: device.sysName ?? device.idxDevice?.toString() ?? "",
      color: "#1E90FF",
      idxDevice: device.idxDevice?.toString(), // custom field for navigation
      title: `
    ${device.sysName ?? "Unknown"}
    Description: ${truncateLines(device.sysDescription ?? "N/A")}
    Hostname: ${device.hostname ?? "N/A"}
    Uptime: ${formatUptime(device.sysUptime)}
  `.trim(), // Tooltip content (HTML-safe string)
    }));
    // Add extra nodes that are not in the current zone
    // These nodes are added with a different color and a tooltip
    // indicating they are not in the current zone
    extraNodesSet.forEach((sysName) => {
      nodesArray.push({
        id: sysName,
        label: sysName,
        color: "#383e44ff",
        title: "Device not in current zone",
      });
    });
    // Set the initial graph state with nodes and edges
    initialGraph.current = { nodes: nodesArray, edges: edgesArray };
    setGraph({ nodes: nodesArray, edges: edgesArray });
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
    // networkRef.current.on("click", (params) => {
    //   if (params.nodes.length === 1) {
    //     const nodeId = params.nodes[0];
    //     const nodeData = nodesData.current?.get(nodeId);
    //     const node = Array.isArray(nodeData) ? nodeData[0] : nodeData;
    //     const idxDevice = (node as any)?.idxDevice ?? nodeId;
    //     const sysName = (node as any)?.label ?? "";
    //     window.location.href = `/devices/${encodeURIComponent(
    //       idxDevice
    //     )}?sysName=${encodeURIComponent(sysName)}#devices-overview`;
    //   }
    // });

    // Node selection highlighting
    networkRef.current.on("selectNode", ({ nodes }) => {
      const selected = nodes[0];
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        const isSelected = node.id === selected;
        nodesData.current!.update({
          id: node.id,
          color: {
            background: isDark ? "#939393ff" : "#D3D3D3",
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
      // Update edges connected to the selected node
      edgesData.current.forEach((edge) => {
        const connected = edge.from === selected || edge.to === selected;
        edgesData.current!.update({
          id: edge.id,
        });
      });
    });
    // Reset node selection highlighting
    networkRef.current.on("deselectNode", () => {
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        nodesData.current!.update({
          id: node.id,
          color: {
            background: isDark ? "#4A90E2" : "#1E90FF",
            border: isDark ? "#999" : "#555",
          },
          font: {
            color: isDark ? "#fff" : "black",
          },
        });
      });
      // Reset edges color
      edgesData.current.forEach((edge) => {
        edgesData.current!.update({
          id: edge.id,
          color: isDark ? "#444" : "#BBBBBB",
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

    // Hide arrow on blur
    networkRef.current.on("blurEdge", (params) => {
      if (!edgesData.current) return;

      edgesData.current.update({
        id: params.edge,
        arrows: { to: false },
      });
    });
  }, [graph, theme]);

  // Effect to handle search term changes
  // When the search term changes, it highlights the matching node and focuses the network view on it.
  // If the node is not found, it logs a warning.
  useEffect(() => {
    if (!searchTerm || !nodesData.current || !networkRef.current) return;

    const node = nodesData.current.get(searchTerm);
    if (!node) {
      console.warn(`Node "${searchTerm}" not found.`);
      return;
    }

    networkRef.current.focus(searchTerm, { scale: 1.5, animation: true });

    nodesData.current.get().forEach((n) => {
      nodesData.current!.update({
        id: n.id,
        color: {
          background: n.id === searchTerm ? "#FF6347" : "#D3D3D3",
          border: "#555",
        },
        font: {
          color: n.id === searchTerm ? "black" : "#A9A9A9",
        },
      });
    });
  }, [searchTerm]);

  const handleReset = () => {
    setSearchTerm("");
    setGraph(initialGraph.current);

    if (!networkRef.current || !nodesData.current || !edgesData.current) return;

    // Clear selection
    networkRef.current.unselectAll();

    // Reset nodes color/font
    nodesData.current.forEach((node) => {
      nodesData.current!.update({
        id: node.id,
        color: { background: "#1E90FF", border: "#555" },
        font: { color: "black" },
      });
    });

    // Reset edges color
    edgesData.current.forEach((edge) => {
      edgesData.current!.update({
        id: edge.id,
        color: "#BBBBBB",
      });
    });

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
    <div>
      <h2 className="text-xl font-semibold mb-2">Network Topology</h2>
      <div className="flex items-center justify-between mb-4 w-full">
        <input
          className="border p-2 rounded mb-4 w-full max-w-sm"
          type="text"
          placeholder="Search device..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <div>
          <button onClick={handleReset} className="reset-button">
            Reset
          </button>
          <button
            onClick={handleExportImage}
            className="text-white rounded ml-4 px-4 py-2 rounded cursor-pointer transition-colors duration-300"
            style={{ backgroundColor: "#CB3CFF" }}
          >
            Export
          </button>
        </div>
      </div>
      <div
        ref={containerRef}
        className="w-full h-[70vh] border rounded shadow"
      />
    </div>
  );
}
