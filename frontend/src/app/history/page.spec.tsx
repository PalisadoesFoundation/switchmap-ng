/// <reference types="vitest" />
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import DeviceHistoryChart from "@/app/history/page"; // adjust path

// Mock fetch
beforeEach(() => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      data: {
        zones: {
          edges: [
            {
              node: {
                idxZone: 1,
                name: "Zone A",
                devices: {
                  edges: [
                    {
                      node: {
                        idxDevice: 101,
                        hostname: "device1",
                        sysName: "sys-1",
                        lastPolled: Math.floor(Date.now() / 1000),
                      },
                    },
                  ],
                },
              },
            },
          ],
        },
      },
    }),
  }) as any;
});

afterEach(() => {
  vi.resetAllMocks();
});

describe("DeviceHistoryChart", () => {
  it("renders header and description", () => {
    render(<DeviceHistoryChart />);
    expect(
      screen.getByRole("heading", { name: /device history/i })
    ).toBeInTheDocument();
    expect(
      screen.getByText(/visualizing the historical movement/i)
    ).toBeInTheDocument();
  });

  it("shows loading state", async () => {
    (global.fetch as any).mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                ok: true,
                json: async () => ({ data: { zones: { edges: [] } } }),
              }),
            100
          )
        )
    );

    render(<DeviceHistoryChart />);
    expect(await screen.findByText(/loading devices/i)).toBeInTheDocument();
  });

  it("shows results after fetch", async () => {
    render(<DeviceHistoryChart />);

    const result = await screen.findByText(
      (_, element) =>
        element?.tagName === "P" &&
        element.textContent?.includes("Showing results for Hostname: device1")
    );

    expect(result).toBeInTheDocument();
  });

  it("allows searching for a device", async () => {
    render(<DeviceHistoryChart />);

    // Wait for initial results
    const initialResult = await screen.findByText(
      (_, element) =>
        element?.tagName === "P" &&
        element.textContent?.includes("Showing results for Hostname: device1")
    );
    expect(initialResult).toBeInTheDocument();

    // Type in search input
    const input = screen.getByPlaceholderText(/search device hostname/i);
    fireEvent.change(input, { target: { value: "device1" } });

    const suggestion = await screen.findByText(
      (_, element) =>
        element?.tagName === "LI" && element.textContent === "device1"
    );
    fireEvent.click(suggestion);

    const updatedResult = await screen.findByText(
      (_, element) =>
        element?.tagName === "P" &&
        element.textContent?.includes("Showing results for Hostname: device1")
    );

    expect(updatedResult).toBeInTheDocument();
  });

  it("allows changing date range", async () => {
    render(<DeviceHistoryChart />);
    const button = await screen.findByRole("button", { name: /past 1 week/i });
    fireEvent.click(button);

    expect(await screen.findByText(/past 1 day/i)).toBeInTheDocument();
    fireEvent.click(screen.getByText(/past 1 day/i));

    expect(await screen.findByRole("button", { name: /past 1 day/i }));
  });
});
