/// <reference types="vitest" />
import React from "react";
import { render, screen } from "@testing-library/react";
import RootLayout from "./layout";

// --- Mock next/font/google ---
vi.mock("next/font/google", () => ({
  Geist: vi.fn(() => ({ variable: "--font-geist-sans" })),
  Geist_Mono: vi.fn(() => ({ variable: "--font-geist-mono" })),
}));

// --- Mock next-themes ---
vi.mock("next-themes", () => ({
  ThemeProvider: ({ children }: any) => <div>{children}</div>,
}));

describe("RootLayout", () => {
  it("renders children inside the layout", () => {
    render(
      <RootLayout>
        <div data-testid="child">Hello</div>
      </RootLayout>
    );
    expect(screen.getByTestId("child")).toBeInTheDocument();
  });
});
