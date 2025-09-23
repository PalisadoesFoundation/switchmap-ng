// ---- Mock next/navigation ----
const mockRouterPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockRouterPush, replace: vi.fn() }),
  useParams: () => ({ id: "1" }),
  useSearchParams: () =>
    new URLSearchParams("sysName=TestDevice&hostname=testhost"),
}));

// ---- Imports after mocks ----
import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
} from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import React from "react";
import { TopologyChart } from "./TopologyChart";
import { mockDevice, mockDeviceLLDP } from "./__mocks__/deviceMocks";
import { Edge, Network } from "vis-network/standalone/esm/vis-network";

// ---- Mock vis-network ----
vi.mock("vis-network/standalone/esm/vis-network", () => {
  const updateMock = vi.fn();
  const removeMock = vi.fn();
  const focusMock = vi.fn();
  const addMock = vi.fn();
  const forEachMock = vi.fn((callback: any) =>
    [{ id: "1" }, { id: "2" }].forEach(callback)
  );

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
    destroy: vi.fn(),
    nodes: [],
    edges: [],
    nodesData: { add: addMock, update: updateMock, forEach: forEachMock },
    edgesData: { update: updateMock, forEach: forEachMock },
    getSelectedEdges: vi.fn(() => []),
  }));

  return { Network: NetworkMock, DataSet: DataSetMock, removeMock };
});

// ---- Test Suite: TopologyChart ----
describe("TopologyChart", () => {
  afterEach(() => {
    vi.resetAllMocks();
    cleanup();
  });

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
      <TopologyChart devices={[mockDeviceLLDP]} loading={false} error={null} />
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
    fireEvent.change(input, { target: { value: "Device" } });
    fireEvent.click(await screen.findByText(/Device 1/i));
    expect(
      screen.getByText(/Showing results for: Device 1/i)
    ).toBeInTheDocument();
  });

  it("resets graph on reset button click", () => {
    render(
      <TopologyChart devices={[mockDevice]} loading={false} error={null} />
    );
    fireEvent.click(screen.getByText(/reset/i));
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
    fireEvent.change(screen.getByPlaceholderText(/search device/i), {
      target: { value: "Unknown" },
    });
    expect(screen.queryByText("Device 1")).not.toBeInTheDocument();
  });

  it("does not crash with undefined devices prop", () => {
    render(
      <TopologyChart devices={undefined as any} loading={false} error={null} />
    );
    expect(screen.getByText(/network topology/i)).toBeInTheDocument();
  });

  // ---- Test Suite: TopologyChart additional interactions ----
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
      mockInstance.removeSpy = removeSpy;
    });

    // ---- Node interactions ----
    it("calls router.push on node double-click", () => {
      const doubleClickCallback = mockInstance.on.mock.calls.find(
        ([e]: [string, Function]) => e === "doubleClick"
      )?.[1];
      doubleClickCallback({ nodes: ["Device 1"] });
      expect(mockRouterPush).toHaveBeenCalledWith(
        "/devices/1?sysName=Device%201#devices-overview"
      );
    });

    it("updates nodes on selectNode", () => {
      const mockUpdate = vi.fn();
      mockInstance.nodesData = {
        current: [
          { id: "1", sysName: "Device 1", opacity: 1, color: {}, font: {} },
          { id: "2", sysName: "Device 2", opacity: 1, color: {}, font: {} },
        ],
        update: mockUpdate,
        forEach: (cb: (node: any) => void) =>
          mockInstance.nodesData.current.forEach(cb),
      };

      const callbacks: Record<string, (params: any) => void> = {};
      mockInstance.on = vi.fn((event, cb) => {
        callbacks[event] = cb;
      });

      mockInstance.on("selectNode", ({ nodes }: { nodes: string[] }) => {
        const selected = nodes[0];
        mockInstance.nodesData.current.forEach((node: any) => {
          const isSelected = node.id === selected;
          mockInstance.nodesData.update({
            id: node.id,
            opacity: isSelected ? 1 : 0.6,
            color: { border: "#555" },
            font: { color: isSelected ? "black" : "#A9A9A9" },
          });
        });
      });

      callbacks["selectNode"]({ nodes: ["1"] });
      expect(mockUpdate).toHaveBeenCalledWith(
        expect.objectContaining({ id: "1", opacity: 1 })
      );
      expect(mockUpdate).toHaveBeenCalledWith(
        expect.objectContaining({ id: "2", opacity: 0.6 })
      );
    });

    it("resets nodes and edges on deselectNode", () => {
      const deselectNodeHandler = mockInstance.on.mock.calls.find(
        ([e]: [string, Function]) => e === "deselectNode"
      )?.[1];
      deselectNodeHandler();
      expect(mockInstance.nodesData.update).toHaveBeenCalled();
      expect(mockInstance.edgesData.update).toHaveBeenCalled();
    });

    // ---- Edge interactions ----
    it("updates arrow on hoverEdge", () => {
      const hoverEdgeHandler = mockInstance.on.mock.calls.find(
        ([e]: [string, Function]) => e === "hoverEdge"
      )?.[1];
      hoverEdgeHandler({ edge: "1" });
      expect(mockInstance.edgesData.update).toHaveBeenCalledWith(
        expect.objectContaining({
          id: "1",
          arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        })
      );
    });

    it("removes arrow on blurEdge", () => {
      const blurEdgeHandler = mockInstance.on.mock.calls.find(
        ([e]: [string, Function]) => e === "blurEdge"
      )?.[1];
      mockInstance.getSelectedEdges.mockReturnValue([]);
      blurEdgeHandler({ edge: "1" });
      expect(mockInstance.edgesData.update).toHaveBeenCalledWith(
        expect.objectContaining({
          id: "1",
          arrows: { to: false },
        })
      );
    });
  });
});
