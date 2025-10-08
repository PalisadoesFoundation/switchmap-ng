// ---- Mock next/navigation ----
const mockRouterPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockRouterPush, replace: vi.fn() }),
  useParams: () => ({ id: "1" }),
  useSearchParams: () =>
    new URLSearchParams("sysName=TestDevice&hostname=testhost"),
}));

// ---- Mock next-themes ----
const mockSetTheme = vi.fn();
const mockTheme = vi.fn(() => "light");
vi.mock("next-themes", () => ({
  useTheme: () => ({ theme: mockTheme(), setTheme: mockSetTheme }),
}));

// ---- Imports after mocks ----
import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
  RenderResult,
} from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach, Mock } from "vitest";
import React from "react";
import { TopologyChart } from "./TopologyChart";
import { mockDevice, mockDeviceLLDP } from "./__mocks__/deviceMocks";
import { DeviceNode } from "@/app/types/graphql/GetZoneDevices";
import { Edge, Network, Node } from "vis-network/standalone/esm/vis-network";

// ---- Mock vis-network ----
interface MockNetworkInstance {
  fit: Mock;
  moveTo: Mock;
  on: Mock;
  focus: Mock;
  unselectAll: Mock;
  destroy: Mock;
  getSelectedEdges: Mock;
  nodesData: {
    add: Mock;
    update: Mock;
    forEach: Mock;
    get: Mock;
    clear: Mock;
  };
  edgesData: {
    add: Mock;
    update: Mock;
    forEach: Mock;
    get: Mock;
    clear: Mock;
  };
}

interface MockDataSetInstance {
  get: Mock;
  add: Mock;
  clear: Mock;
  update: Mock;
  forEach: Mock;
}

const mockNetworkInstance: MockNetworkInstance = {
  fit: vi.fn(),
  moveTo: vi.fn(),
  on: vi.fn(),
  focus: vi.fn(),
  unselectAll: vi.fn(),
  destroy: vi.fn(),
  getSelectedEdges: vi.fn(() => []),
  nodesData: {
    add: vi.fn(),
    update: vi.fn(),
    forEach: vi.fn(),
    get: vi.fn(() => []),
    clear: vi.fn(),
  },
  edgesData: {
    add: vi.fn(),
    update: vi.fn(),
    forEach: vi.fn(),
    get: vi.fn(() => []),
    clear: vi.fn(),
  },
};

const mockDataSetInstance: MockDataSetInstance = {
  get: vi.fn(() => []),
  add: vi.fn(),
  clear: vi.fn(),
  update: vi.fn(),
  forEach: vi.fn(),
};

vi.mock("vis-network/standalone/esm/vis-network", () => {
  const DataSetMock = vi.fn((data?: Node[] | Edge[]) => ({
    ...mockDataSetInstance,
    get: vi.fn(() => data || []),
  }));

  const NetworkMock = vi.fn(() => mockNetworkInstance);

  return { Network: NetworkMock, DataSet: DataSetMock };
});

// ---- Test Suite: TopologyChart ----
describe("TopologyChart", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockTheme.mockReturnValue("light");
  });

  afterEach(() => {
    cleanup();
  });

  // ---- Basic Rendering Tests ----
  describe("Basic Rendering", () => {
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
        <TopologyChart
          devices={[mockDeviceLLDP]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/search device/i)).toBeInTheDocument();
    });

    it("renders with multiple devices", () => {
      const devices = [
        mockDevice,
        { ...mockDevice, id: "2", idxDevice: 2, sysName: "Device 2" },
      ];
      render(<TopologyChart devices={devices} loading={false} error={null} />);
      expect(screen.getByPlaceholderText(/search device/i)).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: /reset/i })
      ).toBeInTheDocument();
    });

    it("does not crash with undefined devices prop", () => {
      render(
        <TopologyChart
          devices={undefined as unknown as DeviceNode[]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("does not crash with empty devices array", () => {
      render(<TopologyChart devices={[]} loading={false} error={null} />);
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("renders instructions text", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      expect(
        screen.getByText(/single-click to select nodes/i)
      ).toBeInTheDocument();
    });

    it("renders export button", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      expect(
        screen.getByRole("button", { name: /export/i })
      ).toBeInTheDocument();
    });
  });

  // ---- Search Functionality Tests ----
  describe("Search Functionality", () => {
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

    it("shows no suggestions for unmatched search", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      fireEvent.change(screen.getByPlaceholderText(/search device/i), {
        target: { value: "Unknown" },
      });
      expect(screen.queryByText("Device 1")).not.toBeInTheDocument();
    });

    it("clears suggestions when input is empty", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      const input = screen.getByPlaceholderText(/search device/i);
      fireEvent.change(input, { target: { value: "Device" } });
      expect(screen.getByText("Device 1")).toBeInTheDocument();
      fireEvent.change(input, { target: { value: "" } });
      expect(screen.queryByText("Device 1")).not.toBeInTheDocument();
    });

    it("submits search on form submit", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      const input = screen.getByPlaceholderText(/search device/i);
      fireEvent.change(input, { target: { value: "Device 1" } });
      const form = input.closest("form");
      fireEvent.submit(form!);
      expect(
        screen.getByText(/Showing results for: Device 1/i)
      ).toBeInTheDocument();
    });

    it("limits suggestions to 5 items", () => {
      const manyDevices = Array.from({ length: 10 }, (_, i) => ({
        ...mockDevice,
        id: `${i}`,
        idxDevice: i,
        sysName: `Device ${i}`,
      }));
      render(
        <TopologyChart devices={manyDevices} loading={false} error={null} />
      );
      const input = screen.getByPlaceholderText(/search device/i);
      fireEvent.change(input, { target: { value: "Device" } });
      const suggestions = screen.getAllByRole("listitem");
      expect(suggestions.length).toBeLessThanOrEqual(5);
    });
  });

  // ---- Reset and Export Tests ----
  describe("Reset and Export Functionality", () => {
    it("resets graph on reset button click", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      fireEvent.click(screen.getByText(/reset/i));
      expect(mockNetworkInstance.unselectAll).toHaveBeenCalled();
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("clears search result on reset", () => {
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      const input = screen.getByPlaceholderText(/search device/i);
      fireEvent.change(input, { target: { value: "Device 1" } });
      const form = input.closest("form");
      fireEvent.submit(form!);
      fireEvent.click(screen.getByText(/reset/i));
      expect(
        screen.queryByText(/Showing results for/i)
      ).not.toBeInTheDocument();
    });

    it("exports image on export button click", () => {
      const mockToDataURL = vi.fn(() => "data:image/png;base64,test");
      const mockCanvas = document.createElement("canvas");
      mockCanvas.toDataURL = mockToDataURL;
      const mockClick = vi.fn();

      const originalCreateElement = document.createElement.bind(document);
      const createSpy = vi
        .spyOn(document, "createElement")
        .mockImplementation((tag: string) => {
          if (tag === "a") {
            const anchor = originalCreateElement("a") as HTMLAnchorElement;
            Object.defineProperty(anchor, "click", {
              value: mockClick,
              writable: true,
            });
            return anchor;
          }
          return originalCreateElement(tag);
        });

      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );

      const container = screen.getByText(/network topology/i).parentElement;
      const canvasContainer = container?.querySelector(
        ".topology-network-canvas"
      );
      if (canvasContainer) {
        canvasContainer.appendChild(mockCanvas);
      }

      fireEvent.click(screen.getByText(/export/i));
      expect(mockToDataURL).toHaveBeenCalledWith("image/png");
      expect(mockClick).toHaveBeenCalled();
      createSpy.mockRestore();
    });
  });

  // ---- Node and Edge Interaction Tests ----
  describe("Node and Edge Interactions", () => {
    let callbacks: Record<string, Function>;

    beforeEach(() => {
      callbacks = {};
      mockNetworkInstance.on.mockImplementation((event, cb) => {
        callbacks[event] = cb;
      });
      mockDataSetInstance.get.mockReturnValue({ id: "Device 1" });
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
    });

    it("calls router.push on node double-click with idxDevice", () => {
      callbacks["doubleClick"]({ nodes: ["Device 1"] });
      expect(mockRouterPush).toHaveBeenCalledWith(
        "/devices/1?sysName=Device%201#devices-overview"
      );
    });

    it("does not navigate on double-click without idxDevice", () => {
      // Re-render with a device missing idxDevice to simulate the case
      cleanup();
      render(
        <TopologyChart
          devices={[{ ...mockDevice, idxDevice: undefined } as any]}
          loading={false}
          error={null}
        />
      );
      callbacks["doubleClick"]({ nodes: ["Device 1"] });
      expect(mockRouterPush).not.toHaveBeenCalled();
    });

    it("does not navigate when no node is double-clicked", () => {
      callbacks["doubleClick"]({ nodes: [] });
      expect(mockRouterPush).not.toHaveBeenCalled();
    });

    it("updates nodes on selectNode", () => {
      const nodes = [{ id: "Device 1" }, { id: "Device 2" }];
      mockDataSetInstance.forEach.mockImplementation(
        (cb: (node: Node) => void) =>
          nodes.forEach(cb as (value: { id: string }) => void)
      );
      callbacks["selectNode"]({ nodes: ["Device 1"] });
      expect(mockDataSetInstance.update).toHaveBeenCalled();
    });

    it("resets nodes and edges on deselectNode", () => {
      callbacks["deselectNode"]();
      expect(mockDataSetInstance.update).toHaveBeenCalled();
    });

    it("updates arrow on hoverEdge", () => {
      callbacks["hoverEdge"]({ edge: "edge-1" });
      expect(mockDataSetInstance.update).toHaveBeenCalledWith(
        expect.objectContaining({
          id: "edge-1",
          arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        })
      );
    });

    it("removes arrow on blurEdge when edge is not selected", () => {
      mockNetworkInstance.getSelectedEdges.mockReturnValue([]);
      callbacks["blurEdge"]({ edge: "edge-1" });
      expect(mockDataSetInstance.update).toHaveBeenCalledWith(
        expect.objectContaining({
          id: "edge-1",
          arrows: { to: false },
        })
      );
    });

    it("keeps arrow on blurEdge when edge is selected", () => {
      mockNetworkInstance.getSelectedEdges.mockReturnValue(["edge-1"]);
      mockDataSetInstance.update.mockClear();
      callbacks["blurEdge"]({ edge: "edge-1" });
      expect(mockDataSetInstance.update).not.toHaveBeenCalled();
    });

    it("updates arrow on selectEdge", () => {
      callbacks["selectEdge"]({ edges: ["edge-1"] });
      expect(mockDataSetInstance.update).toHaveBeenCalledWith(
        expect.objectContaining({
          id: "edge-1",
          arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        })
      );
    });

    it("resets edges on deselectEdge", () => {
      callbacks["deselectEdge"]();
      expect(mockDataSetInstance.update).toHaveBeenCalled();
    });
  });

  // ---- Graph Building Tests ----
  describe("Graph Building", () => {
    it("creates nodes from devices with CDP interfaces", () => {
      const deviceWithCDP: DeviceNode = {
        ...mockDevice,
        l1interfaces: {
          edges: [
            {
              node: {
                cdpcachedeviceid: "RemoteDevice",
                cdpcachedeviceport: "Eth0/1",
                idxL1interface: "",
                idxDevice: 0,
                ifname: "",
                nativevlan: 0,
                ifoperstatus: 0,
                tsIdle: 0,
                ifspeed: 0,
                ifinUcastPkts: null,
                ifoutUcastPkts: null,
                ifinNUcastPkts: null,
                ifoutNUcastPkts: null,
                ifinOctets: null,
                ifoutOctets: null,
                ifinErrors: null,
                ifoutErrors: null,
                ifinDiscards: null,
                ifoutDiscards: null,
                duplex: "",
                trunk: false,
                cdpcacheplatform: "",
                lldpremportdesc: "",
                lldpremsysname: "",
                lldpremsysdesc: "",
                lldpremsyscapenabled: [],
                macports: {
                  edges: [],
                },
              },
            },
          ],
        },
      };
      render(
        <TopologyChart devices={[deviceWithCDP]} loading={false} error={null} />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("creates nodes from devices with LLDP interfaces", () => {
      render(
        <TopologyChart
          devices={[mockDeviceLLDP]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("filters out devices without sysName", () => {
      const invalidDevice: DeviceNode = {
        ...mockDevice,
        sysName: null as unknown as string,
      };
      render(
        <TopologyChart devices={[invalidDevice]} loading={false} error={null} />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("creates extra nodes for devices not in current zone", () => {
      const deviceWithRemote: DeviceNode = {
        ...mockDevice,
        l1interfaces: {
          edges: [
            {
              node: {
                cdpcachedeviceid: "ExternalDevice",
                cdpcachedeviceport: "Eth0/1",
                idxL1interface: "",
                idxDevice: 0,
                ifname: "",
                nativevlan: 0,
                ifoperstatus: 0,
                tsIdle: 0,
                ifspeed: 0,
                ifinUcastPkts: null,
                ifoutUcastPkts: null,
                ifinNUcastPkts: null,
                ifoutNUcastPkts: null,
                ifinOctets: null,
                ifoutOctets: null,
                ifinErrors: null,
                ifoutErrors: null,
                ifinDiscards: null,
                ifoutDiscards: null,
                duplex: "",
                trunk: false,
                cdpcacheplatform: "",
                lldpremportdesc: "",
                lldpremsysname: "",
                lldpremsysdesc: "",
                lldpremsyscapenabled: [],
                macports: {
                  edges: [],
                },
              },
            },
          ],
        },
      };
      render(
        <TopologyChart
          devices={[deviceWithRemote]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("handles devices with both CDP and LLDP interfaces", () => {
      const mixedDevice: DeviceNode = {
        ...mockDevice,
        l1interfaces: {
          edges: [
            {
              node: {
                cdpcachedeviceid: "CDPDevice",
                cdpcachedeviceport: "Eth0/1",
                idxL1interface: "",
                idxDevice: 0,
                ifname: "",
                nativevlan: 0,
                ifoperstatus: 0,
                tsIdle: 0,
                ifspeed: 0,
                ifinUcastPkts: null,
                ifoutUcastPkts: null,
                ifinNUcastPkts: null,
                ifoutNUcastPkts: null,
                ifinOctets: null,
                ifoutOctets: null,
                ifinErrors: null,
                ifoutErrors: null,
                ifinDiscards: null,
                ifoutDiscards: null,
                duplex: "",
                trunk: false,
                cdpcacheplatform: "",
                lldpremportdesc: "",
                lldpremsysname: "",
                lldpremsysdesc: "",
                lldpremsyscapenabled: [],
                macports: {
                  edges: [],
                },
              },
            },
            {
              node: {
                lldpremsysname: "LLDPDevice",
                lldpremportdesc: "Port1",
                idxL1interface: "",
                idxDevice: 0,
                ifname: "",
                nativevlan: 0,
                ifoperstatus: 0,
                tsIdle: 0,
                ifspeed: 0,
                ifinUcastPkts: null,
                ifoutUcastPkts: null,
                ifinNUcastPkts: null,
                ifoutNUcastPkts: null,
                ifinOctets: null,
                ifoutOctets: null,
                ifinErrors: null,
                ifoutErrors: null,
                ifinDiscards: null,
                ifoutDiscards: null,
                duplex: "",
                trunk: false,
                cdpcachedeviceport: "",
                cdpcacheplatform: "",
                lldpremsysdesc: "",
                lldpremsyscapenabled: [],
                macports: {
                  edges: [],
                },
              },
            },
          ],
        },
      };
      render(
        <TopologyChart devices={[mixedDevice]} loading={false} error={null} />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });
  });

  // ---- Theme Tests ----
  describe("Theme Support", () => {
    it("applies dark theme styles", () => {
      mockTheme.mockReturnValue("dark");
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("applies light theme styles", () => {
      mockTheme.mockReturnValue("light");
      render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });
  });

  // ---- Props Tests ----
  describe("Component Props", () => {
    it("respects zoomView prop when true", () => {
      render(
        <TopologyChart
          devices={[mockDevice]}
          loading={false}
          error={null}
          zoomView={true}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("respects zoomView prop when false", () => {
      render(
        <TopologyChart
          devices={[mockDevice]}
          loading={false}
          error={null}
          zoomView={false}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("respects clickToUse prop when true", () => {
      render(
        <TopologyChart
          devices={[mockDevice]}
          loading={false}
          error={null}
          clickToUse={true}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("respects clickToUse prop when false", () => {
      render(
        <TopologyChart
          devices={[mockDevice]}
          loading={false}
          error={null}
          clickToUse={false}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });
  });

  // ---- Cleanup Tests ----
  describe("Cleanup and Memory Management", () => {
    it("destroys network instance on unmount", () => {
      const { unmount } = render(
        <TopologyChart devices={[mockDevice]} loading={false} error={null} />
      );
      unmount();
      expect(mockNetworkInstance.destroy).toHaveBeenCalled();
    });
  });

  // ---- Edge Cases ----
  describe("Edge Cases", () => {
    it("handles device with zero uptime", () => {
      const deviceWithZeroUptime: DeviceNode = { ...mockDevice, sysUptime: 0 };
      render(
        <TopologyChart
          devices={[deviceWithZeroUptime]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("handles device with null uptime", () => {
      const deviceWithNullUptime: DeviceNode = {
        ...mockDevice,
        sysUptime: null as unknown as number,
      };
      render(
        <TopologyChart
          devices={[deviceWithNullUptime]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("handles device without hostname", () => {
      const deviceWithoutHostname: DeviceNode = {
        ...mockDevice,
        hostname: null as unknown as string,
      };
      render(
        <TopologyChart
          devices={[deviceWithoutHostname]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("handles device with empty interfaces array", () => {
      const deviceWithEmptyInterfaces: DeviceNode = {
        ...mockDevice,
        l1interfaces: { edges: [] },
      };
      render(
        <TopologyChart
          devices={[deviceWithEmptyInterfaces]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });

    it("handles special characters in device names", () => {
      const deviceWithSpecialChars: DeviceNode = {
        ...mockDevice,
        sysName: "Device<>\"'&1",
      };
      render(
        <TopologyChart
          devices={[deviceWithSpecialChars]}
          loading={false}
          error={null}
        />
      );
      expect(screen.getByText(/network topology/i)).toBeInTheDocument();
    });
  });
});
