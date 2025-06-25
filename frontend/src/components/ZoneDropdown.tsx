"use client";

import { useEffect, useState, useRef } from "react";

type Zone = { idxZone: string; id: string };

type ZoneDropdownProps = {
  selectedZoneId: string;
  onChange: (zoneId: string) => void;
};

export default function ZoneDropdown({
  selectedZoneId,
  onChange,
}: ZoneDropdownProps) {
  const [zones, setZones] = useState<Zone[]>([]);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchZones = async () => {
      const res = await fetch("http://localhost:7000/switchmap/api/graphql", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: `
            {
              zones {
                edges {
                  node {
                    idxZone
                    id
                  }
                }
              }
            }
          `,
        }),
      });
      const json = await res.json();
      const rawZones = json.data.zones.edges.map((edge: any) => edge.node);
      setZones(rawZones);
    };

    fetchZones();
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selected = zones.find((z) => z.id === selectedZoneId);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="inline-flex justify-between items-center w-48 px-4 py-2 border border-gray-300 rounded-md shadow-sm outline"
      >
        Zone {selected?.idxZone || "Select Zone"}
        <svg
          className={`ml-2 h-5 w-5 transition-transform duration-200 ${
            open ? "rotate-180" : ""
          }`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {open && (
        <div className="absolute mt-1 w-48 rounded-md shadow-lg border border-gray-200 z-10 max-h-60 overflow-auto">
          {zones.map((zone) => (
            <button
              key={zone.id}
              onClick={() => {
                onChange(zone.id);
                setOpen(false);
              }}
              className="block w-full text-left px-4 py-2 hover:bg-blue-950 focus:outline-none"
            >
              Zone {zone.idxZone}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
