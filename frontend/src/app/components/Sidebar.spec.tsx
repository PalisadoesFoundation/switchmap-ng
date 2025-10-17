/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { Sidebar } from "./Sidebar";

vi.mock("next/link", () => ({ default: ({ children }: any) => children }));

// Mock ThemeToggle
vi.mock("@/app/theme-toggle", () => ({
  ThemeToggle: () => <div>ThemeToggle</div>,
}));

describe("Sidebar", () => {
  // ---------- Rendering ----------

  it("renders static sidebar on large screens", () => {
    render(<Sidebar />);
    expect(screen.getByText(/Switchmap-NG/i)).toBeInTheDocument();
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/History/i)).toBeInTheDocument();
    expect(screen.getByText(/Configuration/i)).toBeInTheDocument();
    expect(screen.getByText(/ThemeToggle/i)).toBeInTheDocument();
  });

  // ---------- Interactions ----------

  it("opens slide-in sidebar on hamburger click", () => {
    render(<Sidebar />);
    const button = screen.getByLabelText(/open sidebar/i);
    fireEvent.click(button);

    const networkLink = screen.getAllByText(/Network Topology/i)[0];
    const devicesLink = screen.getAllByText(/Devices Overview/i)[0];

    expect(networkLink).toBeInTheDocument();
    expect(devicesLink).toBeInTheDocument();
  });

  it("closes sidebar when clicking outside", () => {
    render(<Sidebar />);
    const button = screen.getByLabelText(/open sidebar/i);
    fireEvent.click(button);

    fireEvent.mouseDown(document.body);

    expect(screen.queryByLabelText("slide-in sidebar")).toBeNull();
  });

  it("closes sidebar when clicking outside", () => {
    render(<Sidebar />);
    const button = screen.getByLabelText(/open sidebar/i);
    fireEvent.click(button);
    fireEvent.mouseDown(document.body);

    expect(screen.queryByTestId("slide-in-sidebar")).toBeNull();
  });
});
