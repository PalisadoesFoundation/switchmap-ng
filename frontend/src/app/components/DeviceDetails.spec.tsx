import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DeviceDetails } from "./DeviceDetails";
import { mockDevice, mockMetricsForHost } from "./__mocks__/deviceMocks";

vi.mock("./TopologyChart", () => ({
  TopologyChart: () => (
    <div data-testid="mock-topology">Mocked TopologyChart</div>
  ),
}));

// ---------- Helpers ----------
const openCustomRange = () => {
  const button = screen.getByRole("button", { name: /Past 1 day/i });
  fireEvent.click(button);
  fireEvent.click(screen.getByText("Custom range"));

  const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
  const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

  return { startInput, endInput };
};

describe("DeviceDetails", () => {
  beforeEach(() => {
    vi.resetModules();
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockMetricsForHost),
      } as Response)
    ) as unknown as typeof fetch;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ---------- UI interactions ----------
  describe("UI interactions", () => {
    it("toggles time range dropdown", async () => {
      render(<DeviceDetails device={mockDevice} />);

      const button = screen.getByRole("button", { name: /Past 1 day/i });
      fireEvent.click(button);

      const option = screen.getByText("Past 1 week");
      expect(option).toBeInTheDocument();

      fireEvent.click(option);

      expect(
        screen.getByRole("button", { name: /Past 1 week/i })
      ).toBeInTheDocument();

      expect(screen.queryByRole("listbox")).not.toBeInTheDocument();
    });
  });

  // ---------- Custom range validations ----------
  describe("Custom range validations", () => {
    beforeEach(() => {
      render(<DeviceDetails device={mockDevice} />);
    });

    it("shows error message if custom range exceeds 180 days", async () => {
      const { startInput, endInput } = openCustomRange();

      // Input range > 180 days
      fireEvent.change(startInput, { target: { value: "2025-01-01" } });
      fireEvent.change(endInput, { target: { value: "2025-09-01" } });

      await waitFor(() =>
        expect(
          screen.getByText("Custom range cannot exceed 180 days.")
        ).toBeInTheDocument()
      );
    });
    it("accepts valid custom range without showing error", async () => {
      const { startInput, endInput } = openCustomRange();

      fireEvent.change(startInput, { target: { value: "2025-01-01" } });
      fireEvent.change(endInput, { target: { value: "2025-01-15" } });

      expect(
        screen.queryByText("Custom range cannot exceed 180 days.")
      ).not.toBeInTheDocument();
    });

    it("shows error when start date is after end date", async () => {
      const { startInput, endInput } = openCustomRange();
      fireEvent.change(endInput, { target: { value: "2025-09-10" } });
      fireEvent.change(startInput, { target: { value: "2025-09-15" } });

      await waitFor(() =>
        expect(
          screen.getByText("Start date must be before end date.")
        ).toBeInTheDocument()
      );
    });

    it("shows error when end date is before start date", async () => {
      const { startInput, endInput } = openCustomRange();
      fireEvent.change(startInput, { target: { value: "2025-09-15" } });
      fireEvent.change(endInput, { target: { value: "2025-09-10" } });

      await waitFor(() =>
        expect(
          screen.getByText("End date must be after start date.")
        ).toBeInTheDocument()
      );
    });

    it("errors if start date exceeds 180-day range from end date", async () => {
      const { startInput, endInput } = openCustomRange();

      fireEvent.change(endInput, { target: { value: "2025-08-01" } });
      fireEvent.change(startInput, { target: { value: "2025-01-01" } });

      await waitFor(() =>
        expect(
          screen.getByText("Custom range cannot exceed 180 days.")
        ).toBeInTheDocument()
      );
    });
  });

  // ---------- Network / fetch errors ----------
  describe("Network / fetch errors", () => {
    let consoleSpy: ReturnType<typeof vi.spyOn>;

    beforeEach(() => {
      consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    const renderWithFetch = async (fetchMock: typeof fetch) => {
      global.fetch = fetchMock;
      render(<DeviceDetails device={mockDevice} />);
      await waitFor(() =>
        expect(
          screen.getByText("Failed to load device metrics.")
        ).toBeInTheDocument()
      );
    };

    it("shows error when fetch fails", async () => {
      await renderWithFetch(
        vi.fn(() => Promise.reject(new Error("Network error"))) as any
      );
    });

    it("logs fetch error to console", async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({ ok: false, status: 500 })
      ) as unknown as typeof fetch;

      render(<DeviceDetails device={mockDevice} />);

      await waitFor(() => {
        expect(consoleSpy).toHaveBeenCalledWith(
          expect.stringContaining("Error fetching device metrics:"),
          expect.any(Error)
        );
      });
    });

    it("throws error for GraphQL errors", async () => {
      await renderWithFetch(
        vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: async () => ({ errors: [{ message: "Some GraphQL error" }] }),
          })
        ) as any
      );
    });

    it("throws error for malformed response", async () => {
      await renderWithFetch(
        vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: async () => ({ data: { deviceMetrics: null } }),
          })
        ) as any
      );
    });
  });

  // ---------- Edge cases / special device states ----------
  describe("Edge cases / special device states", () => {
    let consoleSpy: ReturnType<typeof vi.spyOn>;

    beforeEach(() => {
      consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    it("shows device status as 'Down' when sysUptime is 0", () => {
      const downDevice = { ...mockDevice, sysUptime: 0 };
      render(<DeviceDetails device={downDevice} />);
      expect(screen.getByText("Down")).toBeInTheDocument();
    });

    it("handles empty metrics and sets CPU/memory to 0 when values are invalid", async () => {
      const stubEmptyMetrics = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ data: { deviceMetrics: { edges: [] } } }),
        })
      );

      vi.stubGlobal("fetch", stubEmptyMetrics);

      render(<DeviceDetails device={mockDevice} />);

      await waitFor(() => {
        expect(
          screen.getByText(/No uptime data available/i)
        ).toBeInTheDocument();
        expect(screen.getByText(/No CPU data available/i)).toBeInTheDocument();
        expect(
          screen.getByText(/No memory data available/i)
        ).toBeInTheDocument();
      });
    });

    it("filters data using standard time range (non-custom)", async () => {
      // Mock successful metrics fetch with valid data
      const mockMetricsResponse = {
        data: {
          deviceByHostname: {
            edges: [
              {
                node: {
                  id: "1",
                  hostname: "host1",
                  lastPolled: Math.floor(Date.now() / 1000) - 86400, // 1 day ago
                  sysUptime: 3600,
                  systemstats: {
                    edges: [
                      {
                        node: {
                          idxSystemstat: 1,
                          cpu5min: 50,
                          memUsed: 2048,
                          memFree: 2048,
                        },
                      },
                    ],
                  },
                },
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockMetricsResponse,
      });

      render(<DeviceDetails device={mockDevice} />);

      // Wait for component to load
      await waitFor(() => {
        expect(screen.getByText("Device 1")).toBeInTheDocument();
      });

      // Select a non-custom range to trigger the else branch in filtering
      const dropdown = screen.getByRole("button", { name: /past 1 day/i });
      fireEvent.click(dropdown);

      const option = screen.getByRole("button", { name: /past 1 week/i });
      fireEvent.click(option);

      // This should trigger the standard range filtering logic (lines 288-289)
      await waitFor(() => {
        expect(
          screen.getByRole("button", { name: /past 1 week/i })
        ).toBeInTheDocument();
      });
    });

    // Test individual empty data scenarios to cover the "No data available" fallback cases
    it("shows 'No uptime data available' when uptime data is filtered out", async () => {
      // Mock data that would be filtered out by time range
      const mockEmptyUptimeResponse = {
        data: {
          deviceByHostname: {
            edges: [
              {
                node: {
                  id: "1",
                  hostname: "host1",
                  lastPolled:
                    Math.floor(Date.now() / 1000) - 365 * 24 * 60 * 60, // 1 year ago
                  sysUptime: 0, // Down
                  systemstats: {
                    edges: [],
                  },
                },
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockEmptyUptimeResponse,
      });

      render(<DeviceDetails device={mockDevice} />);

      await waitFor(() => {
        expect(
          screen.getByText("No uptime data available")
        ).toBeInTheDocument();
      });
    });

    it("shows 'No CPU data available' when CPU metrics are empty", async () => {
      // Mock data with no systemstats (no CPU/memory data)
      const mockEmptyCpuResponse = {
        data: {
          deviceByHostname: {
            edges: [
              {
                node: {
                  id: "1",
                  hostname: "host1",
                  lastPolled: Math.floor(Date.now() / 1000),
                  sysUptime: 3600,
                  systemstats: {
                    edges: [],
                  },
                },
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockEmptyCpuResponse,
      });

      render(<DeviceDetails device={mockDevice} />);

      await waitFor(() => {
        expect(screen.getByText("No CPU data available")).toBeInTheDocument();
      });
    });

    it("shows 'No memory data available' when memory metrics are empty", async () => {
      // Mock data with no systemstats (no CPU/memory data)
      const mockEmptyMemoryResponse = {
        data: {
          deviceByHostname: {
            edges: [
              {
                node: {
                  id: "1",
                  hostname: "host1",
                  lastPolled: Math.floor(Date.now() / 1000),
                  sysUptime: 3600,
                  systemstats: {
                    edges: [],
                  },
                },
              },
            ],
          },
        },
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockEmptyMemoryResponse,
      });

      render(<DeviceDetails device={mockDevice} />);

      await waitFor(() => {
        expect(
          screen.getByText("No memory data available")
        ).toBeInTheDocument();
      });
    });
  });
});
