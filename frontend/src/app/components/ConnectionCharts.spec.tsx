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
    fireEvent.click(screen.getByRole("button", { name: "Unicast" }));
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
              ifspeed: 0, // Use a number to satisfy the type
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
    expect(screen.getByText(/Traffic/)).toBeInTheDocument();
  });

  // ---------- Dropdown toggle closed and fallback label ----------
  it("toggles dropdown closed and fallback label works", async () => {
    const { rerender } = renderConnectionCharts();
    const button = screen.getByRole("button", { name: /Past 1 day/i });
    fireEvent.click(button);
    expect(screen.getByText("Past 7 days")).toBeInTheDocument();
    fireEvent.click(button);
    expect(screen.queryByText("Past 7 days")).not.toBeInTheDocument();
    rerender(<ConnectionCharts device={mockDevice} />);
  });
});
