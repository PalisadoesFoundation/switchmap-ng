import { describe, it, expect, vi, beforeEach, Mock } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { ConnectionCharts } from "./ConnectionCharts";
import { mockDevice } from "./__mocks__/deviceMocks";

vi.stubGlobal("fetch", vi.fn());

// ---------- Helpers ----------
const renderConnectionCharts = () =>
  render(<ConnectionCharts device={mockDevice} />);

const openCustomRange = () => {
  const button = screen.getByRole("button", { name: /Past 1 day/i });
  fireEvent.click(button);
  fireEvent.click(screen.getByText("Custom range"));

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
});
