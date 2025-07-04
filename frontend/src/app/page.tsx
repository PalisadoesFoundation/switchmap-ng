"use client";

import DevicesOverview from "@/app/components/DevicesOverview";
import ZoneDropdown from "@/app/components/ZoneDropdown";
import { useEffect, useState } from "react";
import Sidebar from "@/app/components/Sidebar";

export default function Home() {
  const [zoneId, setZoneId] = useState<string>("");
  useEffect(() => {
    const hash = window.location.hash;
    if (hash) {
      const el = document.querySelector(hash);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, []);
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar />
      {/* Main Content */}
      <main className="flex-1 overflow-y-auto overflow-x-hidden">
        <div className="sticky top-0 z-10 bg-transparent lg:bg-blend-soft-light flex justify-end p-4">
          <ZoneDropdown selectedZoneId={zoneId} onChange={setZoneId} />
        </div>

        <div id="network-topology" className="h-screen mb-8 p-8">
          <h2 className="text-2xl font-bold mb-4">Network Topology</h2>
        </div>
        <div id="devices-overview" className="h-screen p-8">
          <DevicesOverview zoneId={zoneId} />
        </div>
      </main>
    </div>
  );
}
