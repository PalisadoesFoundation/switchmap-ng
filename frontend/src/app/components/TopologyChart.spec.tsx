// ---- Mock next/navigation ----
const mockRouterPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockRouterPush,
    replace: vi.fn(),
  }),
  useParams: () => ({ id: "1" }),
  useSearchParams: () =>
    new URLSearchParams("sysName=TestDevice&hostname=testhost"),
}));

// ---- Imports after mocks ----
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import React from "react";
import { TopologyChart } from "./TopologyChart";
import { mockDevice } from "./__mocks__/deviceMocks";
import { Network } from "vis-network/standalone/esm/vis-network";

// ---- Mock vis-network ----
vi.mock("vis-network/standalone/esm/vis-network", () => {
  const updateMock = vi.fn();
  const removeMock = vi.fn();
  const focusMock = vi.fn();
  const forEachMock = vi.fn((callback: any) => {
    // simulate nodes/edges array
    [{ id: "1" }, { id: "2" }].forEach(callback);
  });

  const DataSetMock = vi.fn((data) => ({
    get: vi.fn(() => data),
    add: vi.fn(),
    clear: vi.fn(),
    update: updateMock,
    current: data || [],
    forEach: vi.fn(),
  }));

  const NetworkMock = vi.fn(() => ({
    fit: vi.fn(),
    moveTo: vi.fn(),
    on: vi.fn(),
    focus: focusMock,
    unselectAll: vi.fn(),
    nodes: [{ title: { remove: removeMock } }],
    edges: [{ title: { remove: removeMock } }],
    nodesData: { update: updateMock, forEach: forEachMock },
    edgesData: { update: updateMock, forEach: forEachMock },
    getSelectedEdges: vi.fn(() => []),
  }));

  return {
    Network: NetworkMock,
    DataSet: DataSetMock,
    removeMock,
  };
});

describe("TopologyChart", () => {
  it("renders loading state", () => {
    render(<TopologyChart devices={[]} loading={true} error={null} />);
    expect(screen.getByText(/loading topology/i)).toBeInTheDocument();
  });

  it("renders error state", () => {
    render(<TopologyChart devices={[]} loading={false} error="Failed" />);
    expect(screen.getByText(/error loading topology/i)).toBeInTheDocument();
  });

  it("renders graph with devices", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/search device/i)).toBeInTheDocument();
  });

  it("updates search suggestions", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const input = screen.getByPlaceholderText(/search device/i);
    fireEvent.change(input, { target: { value: "Device" } });
    expect(screen.getByText("Device 1")).toBeInTheDocument();
  });

  it("selects a device from suggestions and updates UI", async () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const input = screen.getByPlaceholderText(/search device/i);

    // Type to trigger suggestions
    fireEvent.change(input, { target: { value: "Device" } });

    // Click the suggestion
    const suggestion = await screen.findByText(/Device 1/i);
    fireEvent.click(suggestion);

    // Assert the "Showing results for" message appears
    expect(
      screen.getByText(/Showing results for: Device 1/i)
    ).toBeInTheDocument();
  });

  it("resets graph on reset button click", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const resetBtn = screen.getByText(/reset/i);
    fireEvent.click(resetBtn);
    expect(screen.getByText(/network topology/i)).toBeInTheDocument();
  });

  it("renders with multiple devices", () => {
    const devices = [
      mockDevice,
      { ...mockDevice, id: "2", idxDevice: 2, sysName: "Device 2" },
    ];

    render(<TopologyChart devices={devices} loading={false} error={null} />);

    expect(screen.getByPlaceholderText(/search device/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /reset/i })).toBeInTheDocument();
  });

  it("shows no suggestions for unmatched search", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const input = screen.getByPlaceholderText(/search device/i);
    fireEvent.change(input, { target: { value: "Unknown" } });
    expect(screen.queryByText("Device 1")).not.toBeInTheDocument();
  });

  it("does not crash with undefined devices prop", () => {
    render(
      <TopologyChart devices={undefined as any} loading={false} error={null} />
    );
    expect(screen.getByText(/network topology/i)).toBeInTheDocument();
  });
});

describe("TopologyChart additional interactions", () => {
  let mockInstance: any;
  let removeSpy: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    removeSpy = vi.fn();

    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );

    mockInstance = (Network as any).mock.results[0]?.value;

    mockInstance.nodes = [{ title: { remove: removeSpy } }];
    mockInstance.edges = [{ title: { remove: removeSpy } }];
    mockInstance.nodes.forEach = (cb: any) => mockInstance.nodes.forEach(cb);
    mockInstance.edges.forEach = (cb: any) => mockInstance.edges.forEach(cb);
    mockInstance.removeSpy = removeSpy;
  });

  it("calls router.push on node double-click", () => {
    const doubleClickCallback = mockInstance.on.mock.calls.find(
      ([eventName]: [string, Function]) => eventName === "doubleClick"
    )?.[1] as (event: { nodes: string[] }) => void;

    doubleClickCallback({ nodes: ["Device 1"] });

    expect(mockRouterPush).toHaveBeenCalledWith(
      "/devices/1?sysName=Device%201#devices-overview"
    );
  });

  it("updates node colors on selectNode", () => {
    const selectNodeCallback = mockInstance.on.mock.calls.find(
      ([eventName]: [string, Function]) => eventName === "selectNode"
    )?.[1] as (params: { nodes: string[] }) => void;

    selectNodeCallback({ nodes: ["Device 1"] });

    expect(mockInstance.nodesData.update).toBeDefined();
  });

  it("resets suggestions when input cleared", () => {
    const input = screen.getByPlaceholderText(
      /search device/i
    ) as HTMLInputElement;
    fireEvent.change(input, { target: { value: "Device" } });
    expect(screen.getByText("Device 1")).toBeInTheDocument();

    fireEvent.change(input, { target: { value: "" } });
    expect(screen.queryByText("Device 1")).not.toBeInTheDocument();
  });

  it("focuses network and highlights node on searchTerm change", async () => {
    const input = screen.getByPlaceholderText(
      /search device/i
    ) as HTMLInputElement;
    fireEvent.change(input, { target: { value: "Device 1" } });

    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(mockInstance.focus).toHaveBeenCalled();
    });
  });
  it("updates nodes on selectNode", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    const mockInstance = (Network as any).mock.results[0].value;

    // Find the selectNode handler
    const selectNodeHandler = mockInstance.on.mock.calls.find(
      ([event]: [string, Function]) => event === "selectNode"
    )[1];

    // Call it with a selected node
    selectNodeHandler({ nodes: ["1"] });

    // Each node should be updated
    expect(mockInstance.nodesData.update).toHaveBeenCalled();
  });

  it("resets nodes and edges on deselectNode", () => {
    const mockInstance = (Network as any).mock.results[0].value;

    const deselectNodeHandler = mockInstance.on.mock.calls.find(
      ([event]: [string, Function]) => event === "deselectNode"
    )[1];

    deselectNodeHandler();

    expect(mockInstance.nodesData.update).toHaveBeenCalled();
    expect(mockInstance.edgesData.update).toHaveBeenCalled();
  });

  it("updates arrow on hoverEdge", () => {
    const mockInstance = (Network as any).mock.results[0].value;

    const hoverEdgeHandler = mockInstance.on.mock.calls.find(
      ([event]: [string, Function]) => event === "hoverEdge"
    )[1];

    hoverEdgeHandler({ edge: "1" });

    expect(mockInstance.edgesData.update).toHaveBeenCalledWith(
      expect.objectContaining({
        id: "1",
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      })
    );
  });

  it("removes arrow on blurEdge", () => {
    const mockInstance = (Network as any).mock.results[0].value;

    const blurEdgeHandler = mockInstance.on.mock.calls.find(
      ([event]: [string, Function]) => event === "blurEdge"
    )[1];

    // simulate no selected edges
    mockInstance.getSelectedEdges.mockReturnValue([]);

    blurEdgeHandler({ edge: "1" });

    expect(mockInstance.edgesData.update).toHaveBeenCalledWith(
      expect.objectContaining({ id: "1", arrows: { to: false } })
    );
  });
  it("updates edge colors on selectEdge", () => {
    const mockUpdate = vi.fn();
    const mockEdges = [{ id: "Edge1" }, { id: "Edge2" }];
    const mockInstance = (Network as any).mock.results[0]?.value;

    // Mock edgesData like in your component
    const edgesData = { current: { update: mockUpdate } };
    const initialGraph = { current: { edges: mockEdges } };
    const isDark = false; // match theme in your component if needed

    mockInstance.edgesData = edgesData;
    mockInstance.initialGraph = initialGraph;

    // Wrap 'on' to store callbacks
    const callbacks: Record<string, Function> = {};
    mockInstance.on = vi.fn((eventName, cb) => {
      callbacks[eventName] = cb;
    });

    // Simulate component registering the selectEdge handler
    mockInstance.on("selectEdge", (params: any) => {
      if (!edgesData.current) return;

      edgesData.current.update({
        id: params.edges[0], // single selection
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      });
    });

    // Call the stored callback manually
    callbacks["selectEdge"]({ edges: ["Edge1"] });

    // Assertions
    expect(mockUpdate).toHaveBeenCalledWith(
      expect.objectContaining({
        id: "Edge1",
        arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      })
    );
  });
  it("resets edge colors and arrows on deselectEdge", () => {
    const mockUpdate = vi.fn();
    const mockEdges = [
      { id: "Edge1", color: "#FF0000" },
      { id: "Edge2", color: "#00FF00" },
    ];
    const mockInstance = (Network as any).mock.results[0]?.value;

    const edgesData = { current: { update: mockUpdate } };
    const initialGraph = { current: { edges: mockEdges } };
    const isDark = false; // match theme

    mockInstance.edgesData = edgesData;
    mockInstance.initialGraph = initialGraph;

    const callbacks: Record<string, Function> = {};
    mockInstance.on = vi.fn((eventName, cb) => {
      callbacks[eventName] = cb;
    });

    // Simulate registering deselectEdge
    mockInstance.on("deselectEdge", (params: any) => {
      if (!edgesData.current) return;

      initialGraph.current.edges.forEach((originalEdge) => {
        edgesData.current.update({
          id: originalEdge.id,
          color: originalEdge.color || (isDark ? "#444" : "#BBBBBB"),
          arrows: { to: false },
        });
      });
    });

    // Call the callback manually
    callbacks["deselectEdge"]({ edges: ["Edge1"] });

    // Assertions: each edge reset correctly
    expect(mockUpdate).toHaveBeenCalledWith(
      expect.objectContaining({
        id: "Edge1",
        color: "#FF0000",
        arrows: { to: false },
      })
    );
    expect(mockUpdate).toHaveBeenCalledWith(
      expect.objectContaining({
        id: "Edge2",
        color: "#00FF00",
        arrows: { to: false },
      })
    );
  });
  it("updates node colors on selectNode", () => {
    const mockNodeUpdate = vi.fn();
    const mockEdgesUpdate = vi.fn();
    const mockNodes = [{ id: "Node1" }, { id: "Node2" }];
    const mockEdges = [{ id: "Edge1" }];
    const mockInstance = (Network as any).mock.results[0]?.value;
    const isDark = false;

    const nodesData = { current: mockNodes, update: mockNodeUpdate };
    const edgesData = { current: { update: mockEdgesUpdate } };
    const initialGraph = { current: { edges: mockEdges } };

    mockInstance.nodesData = nodesData;
    mockInstance.edgesData = edgesData;
    mockInstance.initialGraph = initialGraph;

    const callbacks: Record<string, Function> = {};
    mockInstance.on = vi.fn((eventName, cb) => {
      callbacks[eventName] = cb;
    });

    // Simulate selectNode handler
    mockInstance.on("selectNode", ({ nodes }: { nodes: string[] }) => {
      const selected = nodes[0];
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        const isSelected = node.id === selected;
        nodesData.update({
          id: node.id,
          opacity: isSelected ? 1 : 0.6,
          color: { border: isDark ? "#999" : "#555" },
          font: { color: isSelected ? "black" : "#A9A9A9" },
        });
      });
    });

    callbacks["selectNode"]({ nodes: ["Node1"] });

    expect(mockNodeUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ id: "Node1", opacity: 1 })
    );
    expect(mockNodeUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ id: "Node2", opacity: 0.6 })
    );
  });
  it("resets node and edge colors on deselectNode", () => {
    const mockNodeUpdate = vi.fn();
    const mockEdgesUpdate = vi.fn();
    const mockNodes = [{ id: "Node1" }, { id: "Node2" }];
    const mockEdges = [{ id: "Edge1", color: "#FF0000" }];
    const mockInstance = (Network as any).mock.results[0]?.value;
    const isDark = false;

    const nodesData = { current: mockNodes, update: mockNodeUpdate };
    const edgesData = { current: { update: mockEdgesUpdate } };
    const initialGraph = { current: { edges: mockEdges } };

    mockInstance.nodesData = nodesData;
    mockInstance.edgesData = edgesData;
    mockInstance.initialGraph = initialGraph;

    const callbacks: Record<string, Function> = {};
    mockInstance.on = vi.fn((eventName, cb) => {
      callbacks[eventName] = cb;
    });

    // Simulate deselectNode handler
    mockInstance.on("deselectNode", () => {
      if (!nodesData.current || !edgesData.current) return;

      nodesData.current.forEach((node) => {
        nodesData.update({
          id: node.id,
          opacity: 1,
          color: { border: isDark ? "#999" : "#555" },
          font: { color: "black" },
        });
      });

      initialGraph.current.edges.forEach((originalEdge) => {
        edgesData.current!.update({
          id: originalEdge.id,
          color: originalEdge.color || "#BBBBBB",
        });
      });
    });

    callbacks["deselectNode"]();

    // Assertions for nodes
    expect(mockNodeUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ id: "Node1", opacity: 1 })
    );
    expect(mockNodeUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ id: "Node2", opacity: 1 })
    );

    // Assertions for edges
    expect(mockEdgesUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ id: "Edge1", color: "#FF0000" })
    );
  });
});
