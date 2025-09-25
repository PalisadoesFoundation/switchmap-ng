import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ConnectionDetails } from "./ConnectionDetails";
import { mockDevice } from "./__mocks__/deviceMocks";

vi.mock("next/navigation", () => ({ useParams: () => ({ deviceId: "1" }) }));

describe("ConnectionDetails Component", () => {
  // ---------- Empty / null device ----------
  it("renders no data message when device is null", () => {
    render(<ConnectionDetails device={null as any} />);
    expect(
      screen.getByText(/no interface data available/i)
    ).toBeInTheDocument();
  });

  // ---------- Table rendering ----------
  it("renders table with device interfaces", () => {
    render(<ConnectionDetails device={mockDevice} />);
    expect(screen.getByText(/connection details/i)).toBeInTheDocument();
    expect(screen.getByText("Port")).toBeInTheDocument();
    expect(screen.getByText("VLAN")).toBeInTheDocument();
    expect(screen.getByText("Mac Address")).toBeInTheDocument();
  });

  // ---------- MAC / Manufacturer extraction ----------
  it("extracts MAC addresses correctly", () => {
    render(<ConnectionDetails device={mockDevice} />);
    expect(
      screen.getByText((content) => content.includes("00:11:22:33:44:55"))
    ).toBeInTheDocument();
  });

  it("extracts manufacturers correctly", () => {
    render(<ConnectionDetails device={mockDevice} />);
    expect(
      screen.getByText((content) => content.includes("Cisco"))
    ).toBeInTheDocument();
  });

  // ---------- Interface operational status ----------
  it("shows Active for ifoperstatus === 1", () => {
    render(<ConnectionDetails device={mockDevice} />);
    expect(screen.getByText("Active")).toBeInTheDocument();
  });

  it("shows Disabled for ifoperstatus === 2", () => {
    const disabledInterfaceDevice = {
      ...mockDevice,
      l1interfaces: {
        edges: [
          {
            node: {
              ...mockDevice.l1interfaces.edges[0].node,
              ifoperstatus: 2,
            },
          },
        ],
      },
    };
    render(<ConnectionDetails device={disabledInterfaceDevice} />);
    expect(screen.getByText("Disabled")).toBeInTheDocument();
  });

  it("shows N/A for undefined or other ifoperstatus", () => {
    const naInterfaceDevice = {
      ...mockDevice,
      l1interfaces: {
        edges: [
          {
            node: {
              ...mockDevice.l1interfaces.edges[0].node,
              ifoperstatus: 3,
            },
          },
        ],
      },
    };
    render(<ConnectionDetails device={naInterfaceDevice} />);
    expect(screen.getByText("N/A")).toBeInTheDocument();
  });

  it("renders '-' when CDP / LLDP data is missing", () => {
    const deviceWithMissingCDP = {
      ...mockDevice,
      l1interfaces: {
        edges: [
          {
            node: {
              ...mockDevice.l1interfaces.edges[0].node,
              cdpcachedeviceport: "",
              lldpremsysname: "",
            },
          },
        ],
      },
    };

    render(<ConnectionDetails device={deviceWithMissingCDP} />);
    expect(screen.getByText("-")).toBeInTheDocument();
  });
});
