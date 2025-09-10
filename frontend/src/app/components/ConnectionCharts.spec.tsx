// ConnectionCharts.test.tsx
import { describe, it, expect, vi, beforeEach, Mock } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { ConnectionCharts } from "./ConnectionCharts";
import { mockDevice } from "./__mocks__/deviceMocks";

vi.stubGlobal("fetch", vi.fn());

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

  it("renders interface names", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    expect(screen.getByText("Connection Charts")).toBeInTheDocument();
    expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
  });

  it("expands and collapses interfaces", async () => {
    render(<ConnectionCharts device={mockDevice} />);

    const ifaceToggle = screen.getByText("Gig1/0/1").closest("div")!;
    fireEvent.click(ifaceToggle);

    // Expanded: "Download" appears
    await waitFor(() =>
      expect(screen.getByText("Download")).toBeInTheDocument()
    );

    // Collapse again
    fireEvent.click(ifaceToggle);

    // After collapse: the expanded content is REMOVED from the DOM
    await waitFor(() =>
      expect(screen.queryByText("Download")).not.toBeInTheDocument()
    );

    // But the interface header still exists
    expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
  });

  it("expands all and collapses all buttons", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    const expandBtn = screen.getByText("Expand All");
    fireEvent.click(expandBtn);
    await waitFor(() =>
      expect(screen.getByText("Download")).toBeInTheDocument()
    );

    const collapseBtn = screen.getByText("Collapse All");
    fireEvent.click(collapseBtn);
    await waitFor(() =>
      expect(screen.queryByText("Download")).not.toBeInTheDocument()
    );
  });

  it("calls fetch with correct hostname", async () => {
    render(<ConnectionCharts device={mockDevice} />);
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

  it("downloads CSV when download button clicked", async () => {
    // Mock URL.createObjectURL
    const createObjectURLSpy = vi.fn(() => "blob:mock");
    const revokeObjectURLSpy = vi.fn();
    vi.stubGlobal("URL", {
      createObjectURL: createObjectURLSpy,
      revokeObjectURL: revokeObjectURLSpy,
    });

    render(<ConnectionCharts device={mockDevice} />);
    fireEvent.click(screen.getByText("Gig1/0/1").closest("div")!);

    await waitFor(() => {
      const downloadBtn = screen.getByText("Download");
      fireEvent.click(downloadBtn);
      expect(createObjectURLSpy).toHaveBeenCalled();
      expect(revokeObjectURLSpy).toHaveBeenCalled();
    });
  });
  it("shows date inputs when timeRange is custom", async () => {
    render(<ConnectionCharts device={mockDevice} />);

    // Open the dropdown
    const dropdownButton = screen.getByRole("button", {
      name: /Past 24 hours/i,
    });
    fireEvent.click(dropdownButton);

    // Select "Custom Date"
    const customOption = screen.getByRole("button", { name: /Custom Date/i });
    fireEvent.click(customOption);

    // Now the date pickers should appear
    const startInput = await screen.findByLabelText("Start Date");
    const endInput = await screen.findByLabelText("End Date");

    expect(startInput).toBeInTheDocument();
    expect(endInput).toBeInTheDocument();

    // Simulate typing dates
    fireEvent.change(startInput, { target: { value: "2025-09-01" } });
    fireEvent.change(endInput, { target: { value: "2025-09-09" } });

    expect((startInput as HTMLInputElement).value).toBe("2025-09-01");
    expect((endInput as HTMLInputElement).value).toBe("2025-09-09");
  });

  it("covers 24h timeRange branch", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    // Default is "24h", so fetch and data processing runs
    await waitFor(() => {
      expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
    });
  });

  it("covers 7d and 30d timeRange branches", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    const dropdownButton = screen.getByRole("button", {
      name: /Past 24 hours/i,
    });

    // 7d
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByRole("button", { name: /Past 7 days/i }));
    await waitFor(() => {
      expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
    });

    // 30d
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByRole("button", { name: /Past 30 days/i }));
    await waitFor(() => {
      expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
    });
  });

  it("covers custom date range branch", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    const dropdownButton = screen.getByRole("button", {
      name: /Past 24 hours/i,
    });

    // Open dropdown and select "Custom Date"
    fireEvent.click(dropdownButton);
    fireEvent.click(screen.getByRole("button", { name: /Custom Date/i }));

    // Inputs appear
    const startInput = await screen.findByLabelText("Start Date");
    const endInput = await screen.findByLabelText("End Date");

    // Set start/end dates
    const today = new Date();
    const yesterday = new Date(today.getTime() - 24 * 3600 * 1000);
    fireEvent.change(startInput, {
      target: { value: yesterday.toISOString().split("T")[0] },
    });
    fireEvent.change(endInput, {
      target: { value: today.toISOString().split("T")[0] },
    });

    await waitFor(() => {
      expect(screen.getByText("Gig1/0/1")).toBeInTheDocument();
    });
  });

  it("fills newData for interfaces", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    // Expand interface to render chart
    const toggle = screen.getByText("Gig1/0/1").closest("div")!;
    fireEvent.click(toggle);

    await waitFor(() => {
      expect(screen.getByText("Download")).toBeInTheDocument();
    });
  });

  it("handles Speed push", async () => {
    render(<ConnectionCharts device={mockDevice} />);
    const toggle = screen.getByText("Gig1/0/1").closest("div")!;
    fireEvent.click(toggle);

    await waitFor(() => {
      expect(screen.getByText("Download")).toBeInTheDocument();
    });
  });

  it("sets error if fetch fails", async () => {
    (fetch as unknown as Mock).mockRejectedValueOnce(
      new Error("Network Error")
    );
    render(<ConnectionCharts device={mockDevice} />);

    // Expand the interface so the "No data available" message can appear
    const toggle = screen.getByText("Gig1/0/1").closest("div")!;
    fireEvent.click(toggle);

    await waitFor(() => {
      expect(screen.getByText(/No data available/i)).toBeInTheDocument();
    });
  });
});
