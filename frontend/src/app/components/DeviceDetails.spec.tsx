import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DeviceDetails } from "./DeviceDetails";
import { mockDevice, mockMetricsForHost } from "./__mocks__/deviceMocks";

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
        json: () => Promise.resolve(mockMetricsForHost),
      } as Response)
    ) as unknown as typeof fetch;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // 1. Basic rendering / happy path
  describe("Basic rendering", () => {
    it("renders charts and shows device status with fetched metrics", async () => {
      render(<DeviceDetails device={mockDevice} />);

      await waitFor(() => {
        expect(screen.getByText("System Status")).toBeInTheDocument();
        expect(screen.getByText("CPU Usage (%)")).toBeInTheDocument();
        expect(screen.getByText("Memory Usage (%)")).toBeInTheDocument();
      });

      expect(screen.getByText("Up")).toBeInTheDocument();
    });
  });

  // 2. UI interactions
  describe("UI interactions", () => {
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
  });

  // 3. Custom range validations
  const openCustomRange = () => {
    const button = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(button);
    fireEvent.click(screen.getByText("Custom range"));

    const startInput = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/end date/i) as HTMLInputElement;

    return { startInput, endInput };
  };
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

    it("filters data correctly when custom range is selected", async () => {
      const { startInput, endInput } = openCustomRange();

      // Set a range that includes mockDevice.lastPolled (1693305600 → 2023-08-30 UTC)
      fireEvent.change(startInput, { target: { value: "2023-08-29" } });
      fireEvent.change(endInput, { target: { value: "2023-08-31" } });

      // Wait for chart to render
      await waitFor(() => {
        expect(screen.getByText("System Status")).toBeInTheDocument();
        expect(screen.getByText("Up")).toBeInTheDocument();
      });
    });
  });

  // 4. Network / fetch errors
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

  // 5. Edge cases / special device states
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
      // Helper to stub fetch with empty metrics
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
  });
});
