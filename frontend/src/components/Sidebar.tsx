"use client";

import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { FiLayout, FiClock, FiSettings } from "react-icons/fi";
import { RxHamburgerMenu } from "react-icons/rx";
import ThemeToggle from "@/app/theme-toggle";

export default function Sidebar() {
  const [open, setOpen] = useState<boolean>(false);
  const sidebarRef = useRef<HTMLDivElement>(null);

  // Close sidebar on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent): void => {
      const target = e.target as Node;
      if (sidebarRef.current && !sidebarRef.current.contains(target)) {
        setOpen(false);
      }
    };

    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [open]);

  // Sidebar content
  const sidebarContent = (
    <nav className="space-y-6">
      <div className="flex flex-row items-center justify-between gap-2">
        <h2 className="text-xl font-semibold">Switchmap-NG</h2>
        <ThemeToggle />
      </div>

      <ul className="list-none space-y-4">
        <li>
          <Link
            href="/"
            className="flex items-center gap-2 font-medium hover:text-primary transition-colors"
          >
            <FiLayout className="icon" />
            <p>Dashboard</p>
          </Link>
          <ul className="pl-6 mt-2 space-y-1 text-sm text-muted-foreground">
            <li className="hover:text-primary">
              <Link href="#network-topology" onClick={() => setOpen(false)}>
                Network Topology
              </Link>
            </li>
            <li className="hover:text-primary">
              <Link href="#devices-overview" onClick={() => setOpen(false)}>
                Devices Overview
              </Link>
            </li>
          </ul>
        </li>
        <li>
          <Link
            href="/history"
            className="flex items-center gap-2 hover:text-primary"
            onClick={() => setOpen(false)}
          >
            <FiClock className="icon" />
            <span>History</span>
          </Link>
        </li>
        <li>
          <Link
            href="/settings"
            className="flex items-center gap-2 hover:text-primary"
            onClick={() => setOpen(false)}
          >
            <FiSettings className="icon" />
            <span>Settings</span>
          </Link>
        </li>
      </ul>
    </nav>
  );

  return (
    <>
      {/* Hamburger button */}
      <button
        className="p-3 text-2xl lg:hidden fixed top-4 left-4 z-50 bg-bg border border-border rounded"
        onClick={() => setOpen(true)}
        aria-label="Open sidebar"
      >
        <RxHamburgerMenu />
      </button>

      {/* Static sidebar for large screens */}
      <aside className="hidden lg:block sticky top-0 left-0 w-60 h-screen border-r border-border lg:p-4">
        {sidebarContent}
      </aside>

      {/* Slide-in sidebar for small/medium screens */}
      {open && (
        <>
          <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" />
          <aside
            ref={sidebarRef}
            className="fixed top-0 left-0 w-60 h-full bg-bg border-r border-border z-50 p-4 shadow-md transition-transform transform lg:hidden"
          >
            {sidebarContent}
          </aside>
        </>
      )}
    </>
  );
}
