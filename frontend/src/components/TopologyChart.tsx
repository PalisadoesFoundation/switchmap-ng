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
    edges: { color: isDark ? "#888" : "#BBB", width: 2 },
    nodes: {
      shape: "dot",
      size: 15,
      color: isDark ? "#4A90E2" : "#1E90FF",
      font: { size: 12, color: isDark ? "#fff" : "black" },
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
     * - If a device has interfaces with a CDP (Cisco Discovery Protocol) target,
     *   those relationships become edges.
     *
     * Custom `title` (tooltip) and `idxDevice` are added to nodes for UX features
     * like tooltips and click navigation.
     */
    if (!devices || devices.length === 0) {
      setGraph({ nodes: [], edges: [] });
      return;
    }

    const nodesSet = new Set<string>();
    const extraNodesSet = new Set<string>();
    const edgesArray: Edge[] = [];

    devices.forEach((device) => {
      const sysName = device?.sysName;
      if (!sysName) return;
      if (extraNodesSet.has(sysName)) {
        // If device is in the current zone, skip adding it
        extraNodesSet.delete(sysName);
        nodesSet.add(sysName);
      }
      nodesSet.add(device.sysName);

      (device.l1interfaces?.edges ?? []).forEach(
        ({ node: iface }: { node: any }) => {
          const target = iface?.cdpcachedeviceid;
          const port = iface?.cdpcachedeviceport;

          if (target) {
            if (!nodesSet.has(target)) {
              extraNodesSet.add(target);
            }
            edgesArray.push({
              from: sysName,
              to: target,
              label: "",
              title: String(port ?? ""),
              color: "#BBBBBB",
            } as Edge);
          }
        }
      );
    });
    const truncateTwoLines = (str: string, max = 100) => {
      // Approximate split into two halves to simulate 2 lines
      if (!str) return "N/A";
      if (str.length <= max) return str;
      return str.slice(0, max / 2) + "\n" + str.slice(max / 2, max) + "...";
    };

    const nodesArray: Node[] = devices.map((device) => ({
      id: device.sysName ?? "",
      label: device.sysName ?? device.idxDevice?.toString() ?? "",
      color: "#1E90FF",
      idxDevice: device.idxDevice?.toString(), // custom field for navigation
      title: `
    ${device.sysName ?? "Unknown"}
    Description: ${truncateTwoLines(device.sysDescription ?? "N/A")}
    Hostname: ${device.hostname ?? "N/A"}
    Uptime: ${formatUptime(device.sysUptime)}
  `.trim(), // ✅ Tooltip content (HTML-safe string)
    }));
    // Add extra nodes that are not in the current zone
    extraNodesSet.forEach((sysName) => {
      nodesArray.push({
        id: sysName,
        label: sysName,
        color: "#383e44ff",
        title: "Device not in current zone",
      });
    });

    initialGraph.current = { nodes: nodesArray, edges: edgesArray };
    setGraph({ nodes: nodesArray, edges: edgesArray });
  }, [devices]);

  useEffect(() => {
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
            background: isSelected
              ? "#FF6347" // selected highlight
              : isDark
              ? "#2c2c2c"
              : "#D3D3D3",
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

      edgesData.current.forEach((edge) => {
        const connected = edge.from === selected || edge.to === selected;
        edgesData.current!.update({
          id: edge.id,
          color: connected
            ? isDark
              ? "#888"
              : "#555"
            : isDark
            ? "#333"
            : "#DDD",
        });
      });
    });

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

      edgesData.current.forEach((edge) => {
        edgesData.current!.update({
          id: edge.id,
          color: isDark ? "#444" : "#BBBBBB",
        });
      });
    });
  }, [graph, theme]);

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
