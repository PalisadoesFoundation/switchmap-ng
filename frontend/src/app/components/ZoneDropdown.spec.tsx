/// <reference types="vitest" />
import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
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

  it("initializes state correctly", () => {
    const onChange = vi.fn();
    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);
    expect(screen.getByRole("button")).toBeInTheDocument();
  });

  it("toggles open state on button click", () => {
    const onChange = vi.fn();
    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);

    const button = screen.getByRole("button");
    const svg = button.querySelector("svg");

    expect(svg).not.toHaveClass("rotate-180");
    fireEvent.click(button);
    expect(svg).toHaveClass("rotate-180");
    fireEvent.click(button);
    expect(svg).not.toHaveClass("rotate-180");
  });

  it("selects first zone if selectedZoneId is null", async () => {
    const onChange = vi.fn();
    const mockZones = [{ id: "1", name: "Zone 1", idxZone: "001" }];

    global.fetch = vi.fn(
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
                        zones: { edges: mockZones.map((z) => ({ node: z })) },
                      },
                    },
                  ],
                },
              },
            }),
        }) as any
    );

    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);

    await waitFor(() => expect(onChange).toHaveBeenCalledWith("1"));
    expect(screen.getByText("Zone 1")).toBeInTheDocument();
  });

  it("sets error state when fetch fails", async () => {
    const onChange = vi.fn();
    global.fetch = vi.fn(() => Promise.reject(new Error("Failed"))) as any;

    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);

    await waitFor(() => {
      expect(screen.getByText(/(Error)/)).toBeInTheDocument();
    });
  });

  it("sets loading state while fetching", async () => {
    let resolveFetch: any;
    global.fetch = vi.fn(
      () =>
        new Promise((res) => {
          resolveFetch = res;
        }) as any
    );

    const onChange = vi.fn();
    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);
    expect(screen.getByText(/\(Loading...\)/)).toBeInTheDocument();

    act(() =>
      resolveFetch({ ok: true, json: () => ({ data: { events: [] } }) })
    );
  });

  it("calls onChange when a zone is clicked", async () => {
    const onChange = vi.fn();
    const mockZones = [{ id: "1", name: "Zone 1", idxZone: "001" }];

    global.fetch = vi.fn(
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
                        zones: { edges: mockZones.map((z) => ({ node: z })) },
                      },
                    },
                  ],
                },
              },
            }),
        }) as any
    );
    render(<ZoneDropdown selectedZoneId={null} onChange={onChange} />);

    await waitFor(() => {
      expect(onChange).toHaveBeenCalledWith("1");
      expect(screen.getByText("Zone 1")).toBeInTheDocument();
    });
  });
});
