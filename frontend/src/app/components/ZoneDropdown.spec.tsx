import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
  within,
} from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { ZoneDropdown } from "./ZoneDropdown";

describe("ZoneDropdown - Unit Tests", () => {
  let originalFetch: any;

  beforeEach(() => {
    originalFetch = global.fetch;
    vi.clearAllMocks();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  const renderDropdown = (onChange = vi.fn()) =>
    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);

  const mockFetch = (zones: { id: string; name: string; idxZone: string }[]) =>
    vi.fn(
      () =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              data: {
                events: {
                  edges: [
                    {
                      node: {
                        zones: { edges: zones.map((z) => ({ node: z })) },
                      },
                    },
                  ],
                },
              },
            }),
        }) as any
    );

  // ---------- Rendering ----------
  it("renders main button", () => {
    renderDropdown();
    expect(screen.getByRole("button")).toBeInTheDocument();
  });

  it("toggles open state on button click", () => {
    renderDropdown();
    const button = screen.getByRole("button");
    const svg = button.querySelector("svg");

    expect(svg).not.toHaveClass("rotate-180");
    fireEvent.click(button);
    expect(svg).toHaveClass("rotate-180");
    fireEvent.click(button);
    expect(svg).not.toHaveClass("rotate-180");
  });

  // ---------- Fetching / Initial State ----------
  it("selects first zone if selectedZoneId is null", async () => {
    const onChange = vi.fn();
    const zones = [{ id: "1", name: "Zone 1", idxZone: "001" }];
    global.fetch = mockFetch(zones);

    renderDropdown(onChange);
    await waitFor(() => expect(onChange).toHaveBeenCalledWith("1"));
    expect(screen.getByText("Zone 1")).toBeInTheDocument();
  });

  it("sets loading state while fetching", async () => {
    let resolveFetch: any;
    global.fetch = vi.fn(
      () =>
        new Promise((res) => {
          resolveFetch = res;
        }) as any
    );

    renderDropdown();
    expect(screen.getByText(/\(Loading...\)/)).toBeInTheDocument();

    act(() =>
      resolveFetch({ ok: true, json: () => ({ data: { events: [] } }) })
    );
  });

  it("sets error state when fetch fails", async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error("Failed"))) as any;
    renderDropdown();
    await waitFor(() =>
      expect(screen.getByText(/(Error)/)).toBeInTheDocument()
    );
  });

  // ---------- Interactions ----------
  it("calls onChange when a zone is clicked", async () => {
    const onChange = vi.fn();
    const zones = [{ id: "1", name: "Zone 1", idxZone: "001" }];
    global.fetch = mockFetch(zones);

    renderDropdown(onChange);
    await waitFor(() => expect(onChange).toHaveBeenCalledWith("1"));
    expect(screen.getByText("Zone 1")).toBeInTheDocument();
  });

  it("closes dropdown when clicking outside", async () => {
    renderDropdown();
    const button = screen.getByRole("button");

    fireEvent.click(button); // open dropdown
    expect(button.querySelector("svg")).toHaveClass("rotate-180");

    fireEvent.mouseDown(document.body); // click outside
    await waitFor(() =>
      expect(button.querySelector("svg")).not.toHaveClass("rotate-180")
    );
  });

  it("renders dropdown options and 'all' button", async () => {
    const onChange = vi.fn();
    const zones = [
      { id: "1", name: "Zone 1", idxZone: "001" },
      { id: "2", name: "Zone 2", idxZone: "002" },
    ];
    global.fetch = mockFetch(zones);

    renderDropdown(onChange);

    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
    const dropdownButton = screen.getByRole("button");
    fireEvent.click(dropdownButton);
    const menu = await screen.findByTestId("zone-dropdown-menu");

    for (const zone of zones) {
      const zoneButton = await within(menu).findByTestId(
        `zone-button-${zone.id}`
      );
      expect(zoneButton).toBeInTheDocument();
    }

    fireEvent.click(await within(menu).findByTestId("zone-button-1"));
    expect(onChange).toHaveBeenCalledWith("1");

    fireEvent.click(dropdownButton); // re-open
    const updatedMenu = await screen.findByTestId("zone-dropdown-menu");
    fireEvent.click(await within(updatedMenu).findByTestId("zone-button-all"));
    expect(onChange).toHaveBeenCalledWith("all");
  });

  // ---------- Error Handling ----------
  it("handles network error when res.ok is false", async () => {
    global.fetch = vi.fn(
      () => Promise.resolve({ ok: false, status: 500 }) as any
    );

    renderDropdown();
    fireEvent.click(screen.getByRole("button"));
    await waitFor(() =>
      expect(screen.getByText("Error: Network error: 500")).toBeInTheDocument()
    );
  });

  it("handles GraphQL errors returned in JSON", async () => {
    global.fetch = vi.fn(
      () =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({ errors: [{ message: "GraphQL failed" }] }),
        }) as any
    );

    renderDropdown();
    fireEvent.click(screen.getByRole("button"));
    await waitFor(() =>
      expect(screen.getByText("Error: GraphQL failed")).toBeInTheDocument()
    );
  });
});
