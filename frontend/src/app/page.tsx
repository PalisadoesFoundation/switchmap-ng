"use client";

import DevicesOverview from "@/app/components/DevicesOverview";
import ZoneDropdown from "@/app/components/ZoneDropdown";
import { useEffect, useState } from "react";
import Sidebar from "@/app/components/Sidebar";

export default function Home() {
  const [zoneId, setZoneId] = useState("Wm9uZTox");
  useEffect(() => {
    const hash = window.location.hash;
    if (hash) {
      const el = document.querySelector(hash);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, []);
  return (
    <div className="flex flex-row h-screen overflow-y-hidden">
      {/* Sidebar */}
      <Sidebar />
      {/* Main Content */}
      <main style={{ overflowY: "auto", flex: 1 }}>
        <div className="sticky top-0 z-10 bg-blend-soft-light flex justify-end p-4 shadow">
          <ZoneDropdown selectedZoneId={zoneId} onChange={setZoneId} />
        </div>

        <div id="network-topology" className="h-screen mb-8 p-8">
          <h2 className="text-2xl font-bold mb-4">Network Topology</h2>
        </div>
        <div id="devices-overview" className="h-screen mb-8 p-8">
          <DevicesOverview zoneId={zoneId} />
        </div>
      </main>
    </div>
  );
}
