/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ThemeToggle } from "./theme-toggle";

const setThemeMock = vi.fn();

// Mock next-themes
vi.mock("next-themes", () => ({
  useTheme: () => ({
    resolvedTheme: "light",
    setTheme: setThemeMock,
  }),
}));

describe("ThemeToggle", () => {
  it("renders without crashing", () => {
    render(<ThemeToggle />);
    const button = screen.getByRole("button", { name: /toggle theme/i });
    expect(button).toBeInTheDocument();
  });

  it("toggles theme on click", () => {
    render(<ThemeToggle />);
    const button = screen.getByRole("button", { name: /toggle theme/i });
    fireEvent.click(button);
    expect(setThemeMock).toHaveBeenCalledWith("dark");
  });
});
