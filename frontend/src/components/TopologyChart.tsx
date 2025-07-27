"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Network,
  DataSet,
  Node,
  Edge,
  Options,
} from "vis-network/standalone/esm/vis-network";

interface TopologyChartProps {
  devices: any[];
  loading: boolean;
  error: string | null;
}

const TopologyChart: React.FC<TopologyChartProps> = ({
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
    layout: { hierarchical: false },
    physics: {
      enabled: true,
      solver: "barnesHut",
      stabilization: { iterations: 100, updateInterval: 25 },
    },
    edges: { color: "#BBBBBB", width: 2 },
    nodes: {
      shape: "dot",
      size: 15,
      color: "#1E90FF",
      font: { size: 12, color: "black" },
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
              label: port,
              color: "#BBBBBB",
            });
          }
        }
      );
    });
    function htmlTitle(html: string) {
      const container = document.createElement("div");
      container.innerHTML = html;
      return container;
    }
    // Create nodes array from devices
    // Each node has an `id`, `label`, `color`, and custom `title
    const nodesArray: Node[] = devices.map((device) => ({
      id: device.sysName ?? "", // use sysName as the node ID (to match edge `cdpcachedeviceid`)
      label: device.sysName ?? device.idxDevice?.toString() ?? "",
      color: "#1E90FF",
      idxDevice: device.idxDevice?.toString(), // custom field for navigation
      title: htmlTitle(
        `<div style="display: flex; align-items: left; gap: 2rem;"><div>
    ${device.sysName ?? "Unknown"}<br>
    ${device.hostname ?? "N/A"}
    </div>
    <h1>
  <span style="display: inline-block; font-size: 2em;">
    ${device.sysUptime && device.sysUptime > 0 ? "🟢" : "🔴"}
  </span>
</h1>

    </div><br>
    <h1 style="margin: 0; font-size: 1.2em; font-weight: bold; color: white;">
  ${formatUptime(device.sysUptime) ?? "N/A"}
  <span style="font-size: 0.4em; font-weight: normal;">Uptime</span>
</h1>

  `.trim()
      ), // Tooltip content (HTML-safe string)
    }));
    // To add descirption to nodes, we can use  Description: ${truncateLines(device.sysDescription ?? "N/A")}
    // Add extra nodes that are not in the current zone
    extraNodesSet.forEach((sysName) => {
      nodesArray.push({
        id: sysName,
        label: sysName,
        color: "#383e44ff",
        title: "Device not in current zone",
      });
    });

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
        nodesData.current!.update({
          id: node.id,
          color: {
            background: node.id === selected ? "#FF6347" : "#D3D3D3",
            border: "#555",
          },
          font: {
            color: node.id === selected ? "black" : "#A9A9A9",
          },
        });
      });

      edgesData.current.forEach((edge) => {
        const connected = edge.from === selected || edge.to === selected;
        edgesData.current!.update({
          id: edge.id,
          color: connected ? "#555" : "#DDD",
        });
      });
    });

    // Reset highlight on deselect
    networkRef.current.on("deselectNode", () => {
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        nodesData.current!.update({
          id: node.id,
          color: { background: "#1E90FF", border: "#555" },
          font: { color: "black" },
        });
      });

      edgesData.current.forEach((edge) => {
        edgesData.current!.update({
          id: edge.id,
          color: "#BBBBBB",
        });
      });
    });
  }, [graph]);

      edgesData.current.update({
        id: params.edge,
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      });
      // const tooltip = document.querySelector(".vis-tooltip") as HTMLElement;
      // if (tooltip) {
      //   tooltip.style.background = "transparent !important";
      // }
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
};

export default TopologyChart;
