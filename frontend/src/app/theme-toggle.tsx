"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { FiSun, FiMoon } from "react-icons/fi";
/**
 * A toggle button to switch between light and dark themes.
 *
 * @remarks
 * This component uses the `next-themes` library to manage theme state and
 * persists the user's preference in local storage. It displays a sun icon
 * when the dark theme is active and a moon icon when the light theme is active.
 *
 * @returns A button element that toggles the theme on click.
 *
 * @see {@link useTheme} from `next-themes` for theme management.
 * @see {@link FiSun} and {@link FiMoon} from `react-icons/fi` for the icons used.
 */

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

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
