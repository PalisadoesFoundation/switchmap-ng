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
});
