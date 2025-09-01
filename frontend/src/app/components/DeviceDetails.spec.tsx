import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { DeviceDetails } from "./DeviceDetails";
import { mockDevice, mockDeviceMetrics } from "./__mocks__/deviceMocks";

// Mock fetch globally
global.fetch = vi.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve(mockDeviceMetrics),
  })
) as any;
// Mock TopologyChart so it doesn't create a real Network
vi.mock("./TopologyChart", () => ({
  TopologyChart: () => <div>Mocked TopologyChart</div>,
}));

describe("DeviceDetails", () => {
  it("renders device overview and metadata correctly", async () => {
    render(<DeviceDetails device={mockDevice} />);

    // Check static elements
    expect(screen.getByText("Device Overview")).toBeInTheDocument();
    expect(screen.getByText("Device 1")).toBeInTheDocument();
    expect(screen.getByText("Test device description")).toBeInTheDocument();
    expect(screen.getByText("host1")).toBeInTheDocument();
    expect(screen.getByText("Up")).toBeInTheDocument();

    // Wait for fetched metrics to update
    await waitFor(() => {
      expect(screen.getAllByText("System Status")[0]).toBeInTheDocument();
      expect(screen.getAllByText("CPU Usage (%)")[0]).toBeInTheDocument();
      expect(screen.getAllByText("Memory Usage (%)")[0]).toBeInTheDocument();
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
});
