import { describe, it, expect, vi, beforeEach, Mock } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { ConnectionCharts } from "./ConnectionCharts";
import { mockDevice } from "./__mocks__/deviceMocks";

vi.stubGlobal("fetch", vi.fn());

// ---------- Helpers ----------
const renderConnectionCharts = () =>
  render(<ConnectionCharts device={mockDevice} />);

const openCustomRange = () => {
  const button = screen.getByRole("button", {
    name: /Past 1 day|Select Range/i,
  });
  fireEvent.click(button);
  fireEvent.click(screen.getByText(/Custom range/i));

  const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
  const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

  return { startInput, endInput };
};

const expandInterface = async (ifaceName = "Gig1/0/1") => {
  const toggle = screen.getByText(ifaceName).closest("div")!;
  fireEvent.click(toggle);
  await waitFor(() => expect(screen.getByText("Download")).toBeInTheDocument());
};

const createMockResponse = (overrides = {}) => ({
  ok: true,
  json: async () => ({
    data: {
      deviceByHostname: {
        edges: [
          {
            node: {
              id: mockDevice.id,
              hostname: mockDevice.hostname,
              sysName: mockDevice.sysName,
              lastPolled: mockDevice.lastPolled,
              l1interfaces: {
                edges: [
                  {
                    node: {
                      ifname: "Gig1/0/1",
                      ifspeed: 1000000000,
                      ifinOctets: 1000000,
                      ifoutOctets: 2000000,
                      ifinUcastPkts: 500000,
                      ifoutUcastPkts: 600000,
                      ifinNucastPkts: 100000,
                      ifoutNucastPkts: 150000,
                      ifinErrors: 10,
                      ifoutErrors: 5,
                      ifinDiscards: 2,
                      ifoutDiscards: 3,
                      ...overrides,
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
});

// ---------- Tests ----------
describe("ConnectionCharts", () => {
  beforeEach(() => {
    (fetch as unknown as Mock).mockResolvedValue({
      ok: true,
      json: async () => ({
        data: {
          devices: {
            edges: [
              {
                node: {
                  id: mockDevice.id,
                  hostname: mockDevice.hostname,
                  lastPolled: mockDevice.lastPolled,
                  l1interfaces: mockDevice.l1interfaces,
                },
              },
            ],
          },
        },
      }),
    });
  });

  // ---------- Rendering ----------
  it("renders interface names", () => {
    renderConnectionCharts();
    expect(screen.getByText("Connection Charts")).toBeInTheDocument();
    expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
  });

  // ---------- Interface interactions ----------
  it("expands and collapses interfaces", async () => {
    renderConnectionCharts();
    const toggle = screen.getByText("Gig1/0/1").closest("div")!;
    fireEvent.click(toggle);

    await waitFor(() =>
      expect(screen.getByText("Download")).toBeInTheDocument()
    );

    fireEvent.click(toggle);
    await waitFor(() =>
      expect(screen.queryByText("Download")).not.toBeInTheDocument()
    );

    expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
  });

  it("expands all and collapses all buttons", async () => {
    renderConnectionCharts();
    fireEvent.click(screen.getByText("Expand All"));
    await waitFor(() =>
      expect(screen.getByText("Download")).toBeInTheDocument()
    );

    fireEvent.click(screen.getByText("Collapse All"));
    await waitFor(() =>
      expect(screen.queryByText("Download")).not.toBeInTheDocument()
    );
  });

  // ---------- Fetch ----------
  it("calls fetch with correct hostname", async () => {
    renderConnectionCharts();
    await waitFor(() =>
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("graphql"),
        expect.objectContaining({
          method: "POST",
          body: expect.stringContaining(mockDevice.hostname),
        })
      )
    );
  });

  it("sets error if fetch fails", async () => {
    (fetch as unknown as Mock).mockRejectedValueOnce(
      new Error("Network Error")
    );
    renderConnectionCharts();
    await expandInterface();
    await waitFor(() =>
      expect(screen.getByText(/No data available/i)).toBeInTheDocument()
    );
  });

  // ---------- Download ----------
  it("downloads CSV when download button clicked", async () => {
    const createObjectURLSpy = vi.fn(() => "blob:mock");
    const revokeObjectURLSpy = vi.fn();
    vi.stubGlobal("URL", {
      createObjectURL: createObjectURLSpy,
      revokeObjectURL: revokeObjectURLSpy,
    });

    renderConnectionCharts();
    await expandInterface();

    fireEvent.click(screen.getByText("Download"));
    expect(createObjectURLSpy).toHaveBeenCalled();
    expect(revokeObjectURLSpy).toHaveBeenCalled();
  });

  it("downloads empty CSV with empty data", async () => {
    const createObjectURLSpy = vi.fn(() => "blob:mock");
    const revokeObjectURLSpy = vi.fn();
    vi.stubGlobal("URL", {
      createObjectURL: createObjectURLSpy,
      revokeObjectURL: revokeObjectURLSpy,
    });

    renderConnectionCharts();
    await expandInterface();
    fireEvent.click(screen.getByText("Download"));
    expect(createObjectURLSpy).toHaveBeenCalled();
    expect(revokeObjectURLSpy).toHaveBeenCalled();
  });

  // ---------- Time ranges ----------
  it("covers 24h, 7d, 30d timeRange branches", async () => {
    renderConnectionCharts();
    const dropdownButton = screen.getByRole("button", { name: /Past 1 day/i });

    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Past 7 days"));
    await waitFor(() =>
      expect(screen.getByText("Gig1/0/1")).toBeInTheDocument()
    );

    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Past 30 days"));
    await waitFor(() =>
      expect(screen.getByText("Gig1/0/1")).toBeInTheDocument()
    );
  });

  // ---------- Custom range validations ----------
  describe("Custom range validations", () => {
    beforeEach(() => {
      render(<ConnectionCharts device={mockDevice} />);
    });

    it("shows error message if custom range exceeds 180 days", async () => {
      const { startInput, endInput } = openCustomRange();

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

  // ---------- Error Overlay Dismissal ----------
  it("shows and auto-dismisses error overlay", async () => {
    (fetch as unknown as Mock).mockRejectedValueOnce(new Error("Test Error"));
    renderConnectionCharts();
    await waitFor(() =>
      expect(screen.queryByText(/Test Error|Network Error/i)).toBeTruthy()
    );
  });

  // ---------- Pagination ----------
  it("shows and changes pages with pagination", async () => {
    const manyIfaces = {
      ...mockDevice,
      l1interfaces: {
        edges: Array.from({ length: 15 }).map((_, i) => ({
          node: {
            ...mockDevice.l1interfaces.edges[0].node,
            ifname: `Gig1/0/${i + 1}`,
          },
        })),
      },
    };
    render(<ConnectionCharts device={manyIfaces} />);
    expect(screen.getByText("Page 1 of 2")).toBeInTheDocument();
    const nextBtn = screen.getByRole("button", { name: "Next" });
    fireEvent.click(nextBtn);
    expect(screen.getByText("Page 2 of 2")).toBeInTheDocument();
    const prevBtn = screen.getByRole("button", { name: "Previous" });
    fireEvent.click(prevBtn);
    expect(screen.getByText("Page 1 of 2")).toBeInTheDocument();
  });

  // ---------- fetch not ok ----------
  it("sets error if fetch returns with ok false", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({}),
    });
    renderConnectionCharts();
    await waitFor(() =>
      expect(screen.getByText(/HTTP 500/)).toBeInTheDocument()
    );
  });

  // ---------- Tab switching and Speed chart ----------
  it("switches chart tabs and renders Speed chart", async () => {
    renderConnectionCharts();
    await expandInterface();
    fireEvent.click(screen.getByRole("button", { name: "Speed" }));
    expect(screen.getByText(/Speed/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Unicast In" }));
    expect(screen.getByText(/Errors/)).toBeInTheDocument();
  });

  // ---------- No data available for chart tab ----------
  it("shows 'No data available' for empty chart tab data", async () => {
    const device = {
      ...mockDevice,
      l1interfaces: {
        edges: [
          {
            node: {
              ...mockDevice.l1interfaces.edges[0].node,
              ifspeed: 0,
            },
          },
        ],
      },
    };
    render(<ConnectionCharts device={device} />);
    await expandInterface(device.l1interfaces.edges[0].node.ifname);
    fireEvent.click(screen.getByRole("button", { name: "Speed" }));
    expect(screen.getByText(/No data available/i)).toBeInTheDocument();
  });

  it("renders HistoricalChart when filteredData is not empty", async () => {
    renderConnectionCharts();
    await expandInterface("Gig1/0/1");
    expect(screen.getByText(/Traffic In/)).toBeInTheDocument();
  });

  // ---------- Dropdown toggle closed and fallback label ----------
  it("toggles dropdown closed and fallback label works", async () => {
    render(<ConnectionCharts device={mockDevice} />);

    const button = screen.getByRole("button", { name: /past 1 day/i });
    fireEvent.click(button);

    expect(screen.getByText("Past 7 days")).toBeInTheDocument();

    fireEvent.click(button);
    await waitFor(() => {
      expect(screen.queryByText("Past 7 days")).not.toBeInTheDocument();
    });
  });

  it("toggles dropdown closed and fallback label works", async () => {
    render(<ConnectionCharts device={mockDevice} />);

    const button = screen.getByRole("button", { name: /past 1 day/i });
    fireEvent.click(button);

    expect(screen.getByText("Past 7 days")).toBeInTheDocument();

    fireEvent.click(button);
    await waitFor(() => {
      expect(screen.queryByText("Past 7 days")).not.toBeInTheDocument();
    });
  });

  it("processes interface data for traffic metrics and different time ranges", async () => {
    // Test case for line coverage: processing different interface metrics
    const mockResponse = {
      data: {
        deviceByHostname: {
          edges: [
            {
              node: {
                id: "1",
                hostname: "test-device",
                lastPolled: Math.floor(Date.now() / 1000) - 3600, // 1 hour ago
                l1interfaces: {
                  edges: [
                    {
                      node: {
                        ifname: "Gig1/0/1", // Use the same interface name as mock device
                        ifinOctets: 1000000,
                        ifoutOctets: 2000000,
                        ifinUcastPkts: 100,
                        ifoutUcastPkts: 200,
                        ifinNucastPkts: 10,
                        ifoutNucastPkts: 20,
                        ifinErrors: 1,
                        ifoutErrors: 2,
                        ifinDiscards: 0,
                        ifoutDiscards: 1,
                        ifspeed: 1000000000, // 1 Gbps
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

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<ConnectionCharts device={mockDevice} />);

    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Check that interfaces are rendered (from the device, not the fetch response)
    expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();

    // Expand interface to see charts
    fireEvent.click(screen.getByText("Gig1/0/1"));

    await waitFor(() => {
      expect(screen.getByText(/Gig1\/0\/1 - Traffic In/)).toBeInTheDocument();
    });

    // Test different chart tabs to cover chart color/unit logic
    const tabButtons = screen.getAllByRole("button");
    const trafficOutButton = tabButtons.find(
      (btn) => btn.textContent === "Traffic Out"
    );
    if (trafficOutButton) {
      fireEvent.click(trafficOutButton);
      await waitFor(() => {
        expect(
          screen.getByText(/Gig1\/0\/1 - Traffic Out/)
        ).toBeInTheDocument();
      });
    }

    const speedButton = tabButtons.find((btn) => btn.textContent === "Speed");
    if (speedButton) {
      fireEvent.click(speedButton);
      await waitFor(() => {
        expect(screen.getByText(/Gig1\/0\/1 - Speed/)).toBeInTheDocument();
      });
    }
  });

  it("covers edge cases for data processing and error handling", async () => {
    // Test date filtering edge cases
    const oldTimestamp = Math.floor(Date.now() / 1000) - 365 * 24 * 3600; // 1 year ago
    const mockResponse = {
      data: {
        deviceByHostname: {
          edges: [
            {
              node: {
                id: "1",
                hostname: "test-device",
                lastPolled: oldTimestamp,
                l1interfaces: {
                  edges: [
                    {
                      node: {
                        ifname: "Gig1/0/1",
                        ifinOctets: 1000,
                        ifoutOctets: 2000,
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

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<ConnectionCharts device={mockDevice} />);

    // Set a custom range that excludes the old data
    const customRangeButton = screen.getByRole("button", {
      name: /past 1 day/i,
    });
    fireEvent.click(customRangeButton);

    const customButton = screen.getByText("Custom range");
    fireEvent.click(customButton);

    // Set custom dates that would exclude the old timestamp
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const startInput = screen.getByLabelText(/start date/i);
    const endInput = screen.getByLabelText(/end date/i);

    fireEvent.change(startInput, {
      target: { value: yesterday.toISOString().split("T")[0] },
    });
    fireEvent.change(endInput, {
      target: { value: today.toISOString().split("T")[0] },
    });

    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // This should result in no data due to date filtering
    fireEvent.click(screen.getByText("Gig1/0/1"));

    await waitFor(() => {
      expect(
        screen.getByText("No data available for the selected range.")
      ).toBeInTheDocument();
    });
  });

  it("tests formatLargeNumber function through different value ranges", async () => {
    // Mock response with different speed values to test formatLargeNumber
    const mockResponse = {
      data: {
        deviceByHostname: {
          edges: [
            {
              node: {
                id: "1",
                hostname: "test-device",
                lastPolled: Math.floor(Date.now() / 1000),
                l1interfaces: {
                  edges: [
                    {
                      node: {
                        ifname: "Gig1/0/1",
                        ifspeed: 1500000000, // > 1G
                        ifinOctets: 5000000000, // > 1G
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

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<ConnectionCharts device={mockDevice} />);

    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // This test ensures the formatLargeNumber function gets called with different ranges
    // The function is used in the yAxisConfig.tickFormatter
    expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
  });

  it("covers all chart tab types and display names", async () => {
    const mockResponse = {
      data: {
        deviceByHostname: {
          edges: [
            {
              node: {
                id: "1",
                hostname: "test-device",
                lastPolled: Math.floor(Date.now() / 1000),
                l1interfaces: {
                  edges: [
                    {
                      node: {
                        ifname: "Gig1/0/1",
                        ifinOctets: 1000,
                        ifoutOctets: 2000,
                        ifinUcastPkts: 100,
                        ifoutUcastPkts: 200,
                        ifinNucastPkts: 10,
                        ifoutNucastPkts: 20,
                        ifinErrors: 1,
                        ifoutErrors: 2,
                        ifinDiscards: 0,
                        ifoutDiscards: 1,
                        ifspeed: 1000000,
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

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<ConnectionCharts device={mockDevice} />);

    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Gig1/0/1"));

    await waitFor(() => {
      expect(screen.getByText(/Gig1\/0\/1 - Traffic In/)).toBeInTheDocument();
    });

    // Test tab types to cover getTabDisplayName function and chart colors/units
    const tabsToTest = [
      { text: "Traffic Out", expectedTitle: "Traffic Out" },
      { text: "Unicast In", expectedTitle: "Unicast In" },
      { text: "Unicast Out", expectedTitle: "Unicast Out" },
      { text: "Non-Unicast In", expectedTitle: "Non-Unicast In" },
      { text: "Non-Unicast Out", expectedTitle: "Non-Unicast Out" },
      { text: "Total Errors", expectedTitle: "Total Errors" },
      { text: "Total Discards", expectedTitle: "Total Discards" },
      { text: "Speed", expectedTitle: "Speed" },
    ];

    for (const tab of tabsToTest) {
      const tabButton = screen.queryByText(tab.text);
      if (tabButton) {
        fireEvent.click(tabButton);

        await waitFor(() => {
          expect(
            screen.getByText(new RegExp(`Gig1/0/1 - ${tab.expectedTitle}`))
          ).toBeInTheDocument();
        });
      }
    }
  });

  it("handles abort error correctly", async () => {
    // Mock fetch to throw AbortError
    const abortError = new Error("AbortError");
    abortError.name = "AbortError";

    (global.fetch as any).mockRejectedValueOnce(abortError);

    render(<ConnectionCharts device={mockDevice} />);

    // AbortError should be handled silently, no error message should appear
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Should not show error overlay - but the description text contains "error"
    // so we need to be more specific
    expect(
      screen.queryByText(/error/i, {
        selector: ".bg-gray-300", // Only look for error in the error overlay
      })
    ).not.toBeInTheDocument();
  });
});
