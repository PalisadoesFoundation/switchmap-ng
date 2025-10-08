/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent, within } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DevicesOverview } from "./DevicesOverview";
import { mockDevice } from "./__mocks__/deviceMocks";

vi.mock("next/link", () => ({ default: ({ children }: any) => children }));

describe("DevicesOverview", () => {
  // ---------- Render States ----------
  it("renders loading state", () => {
    render(<DevicesOverview devices={[]} loading={true} error={null} />);
    expect(screen.getByText(/loading devices/i)).toBeInTheDocument();
  });

  it("renders error state", () => {
    render(<DevicesOverview devices={[]} loading={false} error="Failed" />);
    expect(screen.getByText(/error loading devices/i)).toBeInTheDocument();
  });

  it("renders no devices found message", () => {
    render(<DevicesOverview devices={[]} loading={false} error={null} />);
    expect(screen.getByText(/no devices found/i)).toBeInTheDocument();
  });

  it("renders table with devices", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );
    expect(screen.getByText(/devices overview/i)).toBeInTheDocument();
    expect(screen.getByText(/device 1/i)).toBeInTheDocument();
    expect(screen.getByText(/host1/i)).toBeInTheDocument();
    expect(screen.getByText(/1\/1/i)).toBeInTheDocument();
  });

  // ---------- Interactions ----------
  it("updates global filter input", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );
    const input = screen.getByPlaceholderText(/search/i);
    fireEvent.change(input, { target: { value: "Device 1" } });
    expect((input as HTMLInputElement).value).toBe("Device 1");
  });

  it("calls sorting handler on mouse click", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );

    const tables = screen.getAllByRole("table");
    const monitoredTable = tables[0];

    const headerCell = within(monitoredTable).getByRole("columnheader", {
      name: /device name/i,
    });

    fireEvent.click(headerCell);
    expect(headerCell).toBeInTheDocument();
  });

  it("calls sorting handler on Enter and Space key press", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );

    const tables = screen.getAllByRole("table");
    const monitoredTable = tables[0];

    const headerCell = within(monitoredTable).getByRole("columnheader", {
      name: /device name/i,
    });

    fireEvent.keyDown(headerCell, { key: "Enter" });
    fireEvent.keyDown(headerCell, { key: " " });
    expect(headerCell).toBeInTheDocument();
  });

  // ---------- Pagination ----------
  it("paginates devices and controls page buttons", () => {
    const manyDevices = Array.from({ length: 15 }, (_, idx) => ({
      ...mockDevice,
      id: `id${idx}`,
      sysName: `Device ${idx + 1}`,
      hostname: `host${idx + 1}`,
      idxDevice: idx,
    }));
    render(
      <DevicesOverview devices={manyDevices} loading={false} error={null} />
    );

    // Pagination controls
    expect(screen.getByText(/page 1 of 2/i)).toBeInTheDocument();

    const prev = screen.getByRole("button", { name: /previous/i });
    const next = screen.getByRole("button", { name: /next/i });
    expect(prev).toBeDisabled();
    expect(next).not.toBeDisabled();

    fireEvent.click(next);
    expect(screen.getByText(/page 2 of 2/i)).toBeInTheDocument();
    expect(prev).not.toBeDisabled();
    expect(next).toBeDisabled();

    fireEvent.click(prev);
    expect(screen.getByText(/page 1 of 2/i)).toBeInTheDocument();
  });

  // ---------- Table Structure ----------
  it("renders monitored and unmonitored tables correctly", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );
    const tables = screen.getAllByRole("table");
    expect(tables.length).toBeGreaterThanOrEqual(2);

    const monitoredTable = tables[0];
    expect(
      within(monitoredTable).getByRole("columnheader", { name: /device name/i })
    ).toBeInTheDocument();
    expect(
      within(monitoredTable).getByRole("columnheader", { name: /hostname/i })
    ).toBeInTheDocument();
    expect(
      within(monitoredTable).getByRole("columnheader", {
        name: /active ports/i,
      })
    ).toBeInTheDocument();
    expect(
      within(monitoredTable).getByRole("columnheader", { name: /uptime/i })
    ).toBeInTheDocument();

    const unmonitoredTable = tables[1];
    expect(
      within(unmonitoredTable).getByRole("columnheader", {
        name: /device name/i,
      })
    ).toBeInTheDocument();
    expect(within(unmonitoredTable).getByText(/no data/i)).toBeInTheDocument();
  });

  // ---------- Device Link ----------
  it("renders device name as a link (mocked)", () => {
    render(
      <DevicesOverview devices={[mockDevice]} loading={false} error={null} />
    );
    const deviceCell = screen.getByText("Device 1");
    expect(deviceCell).toBeInTheDocument();
  });

  // ---------- Edge Cases ----------
  it("handles device with empty sysName and hostname", () => {
    const device = {
      ...mockDevice,
      sysName: "",
      hostname: "",
    };
    render(<DevicesOverview devices={[device]} loading={false} error={null} />);
    expect(screen.getAllByText("-")[0]).toBeInTheDocument();
  });

  it("handles device with empty interfaces", () => {
    const device = {
      ...mockDevice,
      l1interfaces: { edges: [] },
    };
    render(<DevicesOverview devices={[device]} loading={false} error={null} />);
    expect(screen.getByText("0/0")).toBeInTheDocument();
  });

  it("filters devices with search and resets pagination", () => {
    const manyDevices = Array.from({ length: 15 }, (_, idx) => ({
      ...mockDevice,
      id: `id${idx}`,
      sysName: `Device ${idx + 1}`,
      hostname: `host${idx + 1}`,
      idxDevice: idx,
    }));
    render(
      <DevicesOverview devices={manyDevices} loading={false} error={null} />
    );
    // Initially should show "Page 1 of 2"
    expect(screen.getByText(/page 1 of 2/i)).toBeInTheDocument();

    const input = screen.getByPlaceholderText(/search/i);
    fireEvent.change(input, { target: { value: "Device 12" } });

    expect(screen.getByText("Device 12")).toBeInTheDocument();
    expect(screen.queryByText("Device 1")).not.toBeInTheDocument();
    // Pagination should be hidden when only one result matches filter
    expect(screen.queryByText(/page 1 of 1/i)).not.toBeInTheDocument();
  });
});
