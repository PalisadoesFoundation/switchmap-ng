import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DeviceDetails } from "./DeviceDetails";
import { mockDevice, mockMetricsForHost } from "./__mocks__/deviceMocks";

// Component-specific mocks
vi.mock("./TopologyChart", () => ({
  TopologyChart: () => (
    <div data-testid="mock-topology">Mocked TopologyChart</div>
  ),
}));
describe("DeviceDetails", () => {
  beforeEach(() => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            data: {
              deviceMetrics: {
                edges: [
                  {
                    node: {
                      hostname: "host1",
                      uptime: 1000,
                      cpuUtilization: 50,
                      memoryUtilization: 30,
                      lastPolled: 1693305600, // mockDevice lastPolled
                    },
                  },
                ],
              },
            },
          }),
      } as Response)
    ) as unknown as typeof fetch;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });
  it("renders charts with fetched metrics", async () => {
    // Mock fetch for this test
    vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockMetricsForHost,
    } as any);

    render(<DeviceDetails device={mockDevice} />);

    // wait for charts to appear
    await waitFor(() => {
      expect(screen.getByText("System Status")).toBeInTheDocument();
      expect(screen.getByText("CPU Usage (%)")).toBeInTheDocument();
      expect(screen.getByText("Memory Usage (%)")).toBeInTheDocument();
    });

    // you can also check status labels for up/down
    expect(screen.getByText("Up")).toBeInTheDocument();
  });
  it("fetches device metrics and updates charts", async () => {
    const mockMetrics = {
      data: {
        deviceMetrics: {
          edges: [
            {
              node: {
                hostname: "host1",
                lastPolled: Math.floor(Date.now() / 1000),
                uptime: 120,
                cpuUtilization: 55,
                memoryUtilization: 40,
              },
            },
          ],
        },
      },
    };

    vi.spyOn(global, "fetch").mockResolvedValueOnce({
      ok: true,
      json: async () => mockMetrics,
    } as any);

    render(<DeviceDetails device={mockDevice} />);

    await waitFor(() => {
      expect(screen.getByText("System Status")).toBeInTheDocument();
      expect(screen.getByText("CPU Usage (%)")).toBeInTheDocument();
      expect(screen.getByText("Memory Usage (%)")).toBeInTheDocument();
    });
  });

  it("toggles time range dropdown", async () => {
    render(<DeviceDetails device={mockDevice} />);

    // initial button text
    const button = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(button);

    // dropdown opens
    const option = screen.getByText("Past 1 week");
    expect(option).toBeInTheDocument();

    // select "Past 1 week"
    fireEvent.click(option);

    // button text updates
    expect(
      screen.getByRole("button", { name: /Past 1 week/i })
    ).toBeInTheDocument();

    // dropdown closed
    expect(screen.queryByRole("listbox")).not.toBeInTheDocument();
  });

  it("shows error message if custom range exceeds 180 days", async () => {
    render(<DeviceDetails device={mockDevice} />);

    // Open dropdown and select custom range
    const button = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(button);
    fireEvent.click(screen.getByText("Custom range"));

    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

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
    render(<DeviceDetails device={mockDevice} />);

    const button = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(button);
    fireEvent.click(screen.getByText("Custom range"));

    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

    fireEvent.change(startInput, { target: { value: "2025-01-01" } });
    fireEvent.change(endInput, { target: { value: "2025-01-15" } });

    expect(
      screen.queryByText("Custom range cannot exceed 180 days.")
    ).not.toBeInTheDocument();
  });

  it("shows error when start date is after end date", async () => {
    render(<DeviceDetails device={mockDevice} />);

    // Open dropdown and select "Custom range"
    const dropdownButton = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Custom range"));

    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;
    fireEvent.change(endInput, { target: { value: "2025-09-10" } });
    fireEvent.change(startInput, { target: { value: "2025-09-15" } });

    await waitFor(() =>
      expect(
        screen.getByText("Start date must be before end date.")
      ).toBeInTheDocument()
    );
  });

  it("shows error when end date is before start date", async () => {
    render(<DeviceDetails device={mockDevice} />);

    const dropdownButton = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Custom range"));

    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

    fireEvent.change(startInput, { target: { value: "2025-09-15" } });
    fireEvent.change(endInput, { target: { value: "2025-09-10" } });

    await waitFor(() =>
      expect(
        screen.getByText("End date must be after start date.")
      ).toBeInTheDocument()
    );
  });

  it("errors if start date exceeds 180-day range from end date", async () => {
    render(<DeviceDetails device={mockDevice} />);

    const dropdownButton = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Custom range"));

    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;
    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;

    fireEvent.change(endInput, { target: { value: "2025-08-01" } });
    fireEvent.change(startInput, { target: { value: "2025-01-01" } });

    await waitFor(() =>
      expect(
        screen.getByText("Custom range cannot exceed 180 days.")
      ).toBeInTheDocument()
    );
  });

  it("filters data correctly when custom range is selected", async () => {
    render(<DeviceDetails device={mockDevice} />);

    // Open the time range dropdown and select "Custom range"
    const dropdownButton = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Custom range"));

    // Set start and end dates to cover mockDevice.lastPolled (1693305600 → 2023-08-30 UTC)
    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

    fireEvent.change(startInput, { target: { value: "2023-08-29" } }); // day before
    fireEvent.change(endInput, { target: { value: "2023-08-31" } }); // day after

    await waitFor(() => {
      // The chart should now show the device metrics
      expect(screen.getByText("System Status")).toBeInTheDocument();
      expect(screen.getByText("Up")).toBeInTheDocument(); // based on value=1
    });
  });
  it("filters data correctly when custom range is selected", async () => {
    render(<DeviceDetails device={mockDevice} />);

    // Open the time range dropdown
    const dropdownButton = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByText("Custom range"));

    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

    // Set a range that includes mockDevice.lastPolled (1693305600 → 2023-08-30 UTC)
    fireEvent.change(startInput, { target: { value: "2023-08-29" } });
    fireEvent.change(endInput, { target: { value: "2023-08-31" } });

    // Wait for chart to render
    await waitFor(() => {
      expect(screen.getByText("System Status")).toBeInTheDocument();
      expect(screen.getByText("Up")).toBeInTheDocument();
    });
  });
  it("shows error when fetch fails", async () => {
    // Mock fetch to throw an error
    global.fetch = vi.fn(() =>
      Promise.reject(new Error("Network error"))
    ) as unknown as typeof fetch;

    render(<DeviceDetails device={mockDevice} />);

    // Wait for error message to appear
    await waitFor(() => {
      expect(
        screen.getByText("Failed to load device metrics.")
      ).toBeInTheDocument();
    });
  });
  it("shows device status as 'Down' when sysUptime is 0", () => {
    const downDevice = { ...mockDevice, sysUptime: 0 };

    render(<DeviceDetails device={downDevice} />);

    expect(screen.getByText("Down")).toBeInTheDocument();
  });
  it("handles empty metrics and sets CPU/memory to 0 when values are invalid", async () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    const mockFetchEmpty = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            data: { deviceMetrics: { edges: [] } }, // triggers hostMetrics.length === 0
          }),
      })
    );

    global.fetch = mockFetchEmpty as unknown as typeof fetch;

    const { rerender } = render(<DeviceDetails device={mockDevice} />);

    await waitFor(() => {
      expect(screen.getByText("No uptime data available")).toBeInTheDocument();
      expect(screen.getByText("No CPU data available")).toBeInTheDocument();
      expect(screen.getByText("No memory data available")).toBeInTheDocument();
    });
  });

  it("logs fetch error to console", async () => {
    // Spy on console.error
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});

    // Mock fetch to trigger an error
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

    consoleSpy.mockRestore(); // clean up spy
  });

  it("throws error for GraphQL errors", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            errors: [{ message: "Some GraphQL error" }],
          }),
      })
    ) as unknown as typeof fetch;

    render(<DeviceDetails device={mockDevice} />);

    await waitFor(() =>
      expect(
        screen.getByText("Failed to load device metrics.")
      ).toBeInTheDocument()
    );
  });

  it("throws error for malformed response", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            data: { deviceMetrics: null }, // or missing edges
          }),
      })
    ) as unknown as typeof fetch;

    render(<DeviceDetails device={mockDevice} />);

    await waitFor(() =>
      expect(
        screen.getByText("Failed to load device metrics.")
      ).toBeInTheDocument()
    );
  });
});
