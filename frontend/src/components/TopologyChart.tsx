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
  const [graph, setGraph] = useState<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });
  const [searchTerm, setSearchTerm] = useState("");
  const containerRef = useRef<HTMLDivElement | null>(null);
  const networkRef = useRef<Network | null>(null);
  const nodesData = useRef<DataSet<Node> | null>(null);
  const edgesData = useRef<DataSet<Edge> | null>(null);
  const initialGraph = React.useRef<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });
  const options: Options = {
    layout: { hierarchical: false },
    physics: {
      enabled: true,
      solver: "barnesHut",
      stabilization: { iterations: 100, updateInterval: 25 },
    },
    edges: { color: "text-text", width: 2 },
    nodes: {
      shape: "dot",
      size: 15,
      color: "text-text",
      font: { size: 12, color: "text-text" },
    },
    interaction: {
      hover: true,
      tooltipDelay: 100,
      dragNodes: true,
      zoomView: true,
    },
  };

  useEffect(() => {
    if (!devices || devices.length === 0) {
      setGraph({ nodes: [], edges: [] });
      return;
    }

    const nodesSet = new Set<string>();
    const edgesArray: Edge[] = [];

    devices.forEach((device) => {
      const sysName = device?.sysName;
      if (!sysName) return;

      nodesSet.add(sysName);

      (device.l1interfaces?.edges ?? []).forEach(
        ({ node: iface }: { node: any }) => {
          const target = iface?.cdpcachedeviceid;
          const port = iface?.cdpcachedeviceport;

          if (target) {
            nodesSet.add(target);
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

    const nodesArray: Node[] = devices.map((device) => ({
      id: device.sysName ?? "",
      label: device.sysName ?? device.idxDevice?.toString() ?? "",
      color: "#1E90FF",
      idxDevice: device.idxDevice?.toString(), // custom field for navigation
    }));

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

  if (loading) return <p>Loading topology...</p>;
  if (error) return <p>Error loading topology: {error}</p>;

  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Network Topology</h2>
      <div className="flex items-center justify-between mb-4 w-full">
        <input
          className="border p-2 rounded mb-4 w-full max-w-sm"
          type="text"
          placeholder="Search node ID..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button
          onClick={handleReset}
          className="mb-4 ml-2 px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          Reset
        </button>
      </div>
      <div
        ref={containerRef}
        className="w-full h-[70vh] border rounded shadow"
      />
    </div>
  );
}
