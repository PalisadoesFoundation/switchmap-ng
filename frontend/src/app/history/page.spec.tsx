/// <reference types="vitest" />
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import DeviceHistoryChart from "@/app/history/page";

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
        !!(
          element?.tagName === "P" &&
          element.textContent?.includes("Showing results for Hostname: device1")
        )
    );

    expect(result).toBeInTheDocument();
  });

  it("allows searching for a device", async () => {
    render(<DeviceHistoryChart />);

    // Wait for initial results
    const initialResult = await screen.findByText(
      (_, element) =>
        !!(
          element?.tagName === "P" &&
          element.textContent?.includes("Showing results for Hostname: device1")
        )
    );
    expect(initialResult).toBeInTheDocument();

    // Type in search input
    const input = screen.getByPlaceholderText(/search device hostname/i);
    fireEvent.change(input, { target: { value: "device1" } });

    const suggestion = await screen.findByText(
      (_, element) =>
        !!(element?.tagName === "LI" && element.textContent === "device1")
    );
    fireEvent.click(suggestion);

    const updatedResult = await screen.findByText(
      (_, element) =>
        !!(
          element?.tagName === "P" &&
          element.textContent?.includes("Showing results for Hostname: device1")
        )
    );

    expect(updatedResult).toBeInTheDocument();
  });

  it("allows changing date range", async () => {
    render(<DeviceHistoryChart />);

    // open the menu
    const button = await screen.findByRole("button", { name: /past 1 week/i });
    fireEvent.click(button);

    // pick 1 day
    fireEvent.click(await screen.findByText(/past 1 day/i));
    expect(
      await screen.findByRole("button", { name: /past 1 day/i })
    ).toBeInTheDocument();

    // pick 1 month
    fireEvent.click(screen.getByRole("button", { name: /past 1 day/i }));
    fireEvent.click(await screen.findByText(/past 1 month/i));
    expect(
      await screen.findByRole("button", { name: /past 1 month/i })
    ).toBeInTheDocument();

    // pick 6 months
    fireEvent.click(screen.getByRole("button", { name: /past 1 month/i }));
    fireEvent.click(await screen.findByText(/past 6 months/i));
    expect(
      await screen.findByRole("button", { name: /past 6 months/i })
    ).toBeInTheDocument();
  });

  it("shows an error when custom range exceeds 180 days", async () => {
    render(<DeviceHistoryChart />);

    // Open range selector and choose custom
    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    // Set end date first
    fireEvent.change(endInput, { target: { value: "2025-08-01" } });
    // Then set start date to trigger the >180 days validation
    fireEvent.change(startInput, { target: { value: "2025-01-01" } });

    expect(
      await screen.findByText(/custom range cannot exceed 180 days/i)
    ).toBeInTheDocument();
  });

  it("accepts a valid custom date range without showing an error", async () => {
    render(<DeviceHistoryChart />);

    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    fireEvent.change(startInput, { target: { value: "2025-01-01" } });
    fireEvent.change(endInput, { target: { value: "2025-01-15" } });

    expect(
      screen.queryByText(/custom range cannot exceed 180 days/i)
    ).not.toBeInTheDocument();
  });
  it("shows an error when fetch fails", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("boom"));
    render(<DeviceHistoryChart />);
    expect(await screen.findByText(/boom/i)).toBeInTheDocument();
  });

  it("does not set error when unmounted before fetch fails", async () => {
    let rejectFn!: (err: any) => void;
    const p = new Promise((_resolve, reject) => {
      rejectFn = reject;
    });
    (global.fetch as any).mockReturnValueOnce(p as any);

    const { unmount } = render(<DeviceHistoryChart />);
    unmount();

    // trigger rejection after unmount
    rejectFn(new Error("late failure"));
    await Promise.resolve(); // let microtasks run

    await waitFor(() => {
      expect(
        screen.queryByText(/error fetching devices/i)
      ).not.toBeInTheDocument();
    });
  });
  it("does not search when input is empty", async () => {
    render(<DeviceHistoryChart />);

    const form = screen.getByRole("form");
    const input = screen.getByPlaceholderText(/search device hostname/i);
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.submit(form);
    expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument();
  });
  it("submits search term when input is non-empty", async () => {
    render(<DeviceHistoryChart />);

    const form = screen.getByRole("form");
    const input = screen.getByPlaceholderText(/search device hostname/i);

    fireEvent.change(input, { target: { value: "device1" } });
    fireEvent.submit(form);
    expect(input).toHaveValue("");
    expect(screen.queryByTestId("suggestions-list")).not.toBeInTheDocument();
  });
  it("renders error UI and allows retry", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("boom"));

    // mock reload
    const reloadMock = vi.fn();
    Object.defineProperty(window, "location", {
      configurable: true,
      value: { ...window.location, reload: reloadMock },
    });

    render(<DeviceHistoryChart />);

    expect(await screen.findByText(/error/i)).toBeInTheDocument();
    expect(await screen.findByText(/boom/i)).toBeInTheDocument();
  });

  it("shows an error when end date is before start date", async () => {
    render(<DeviceHistoryChart />);

    // Open range selector and choose custom
    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    // Set start first
    fireEvent.change(startInput, { target: { value: "2025-08-01" } });
    // Set end date before start to trigger validation
    fireEvent.change(endInput, { target: { value: "2025-01-01" } });

    expect(
      await screen.findByText(/end date must be after start date/i)
    ).toBeInTheDocument();
  });

  it("shows an error when custom range exceeds 180 days", async () => {
    render(<DeviceHistoryChart />);

    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    fireEvent.change(startInput, { target: { value: "2025-01-01" } });
    fireEvent.change(endInput, { target: { value: "2025-08-01" } }); // >180 days

    expect(
      await screen.findByText(/custom range cannot exceed 180 days/i)
    ).toBeInTheDocument();
  });
  it("shows an error when start date is after end date", async () => {
    render(<DeviceHistoryChart />);

    // Open range selector and choose custom
    const rangeButton = await screen.findByRole("button", {
      name: /past 1 week/i,
    });
    fireEvent.click(rangeButton);
    fireEvent.click(screen.getByText(/custom/i));

    const startInput = screen.getByLabelText("custom start date");
    const endInput = screen.getByLabelText("custom end date");

    // Set end date first
    fireEvent.change(endInput, { target: { value: "2025-01-01" } });
    // Then set start date after end to trigger the validation
    fireEvent.change(startInput, { target: { value: "2025-08-01" } });

    expect(
      await screen.findByText(/start date must be before end date/i)
    ).toBeInTheDocument();
  });
});
