"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { FiSun, FiMoon } from "react-icons/fi";
/**
 * ThemeToggle component allows users to switch between light and dark themes.
 * It uses the Next.js `useTheme` hook to manage the theme state.
 * The component renders a button that toggles the theme when clicked.
 *
 * @remarks
 * This component is designed for client-side use only because it relies on
 * the `useTheme` hook, which is not available during server-side rendering.
 * It also ensures the component is mounted before rendering to avoid SSR mismatches.
 * The icons used for the toggle come from the `react-icons` library.
 *
 * @returns The rendered component.
 *
 * @see {@link useTheme} for managing themes in Next.js.
 * @see {@link FiSun} and {@link FiMoon} for the icons used in the toggle button.
 */

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null; // prevent SSR mismatch

  return (
    <button
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      aria-label="Toggle theme"
      className="bg-transparent text-[1.4rem] flex self-center"
    >
      {resolvedTheme === "dark" ? <FiSun /> : <FiMoon />}
    </button>
  );
}
