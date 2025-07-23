"use client";

import DevicesOverview from "@/app/components/DevicesOverview";
import ZoneDropdown from "@/app/components/ZoneDropdown";
import { useEffect, useState } from "react";
import Sidebar from "@/app/components/Sidebar";

function Home() {
  const [zoneId, setZoneId] = useState("");
  const [zoneSelected, setZoneSelected] = useState(false);
  useEffect(() => {
    // Load zoneId from localStorage on mount
    try {
      setZoneId(localStorage.getItem("zoneId") || "");
    } catch (error) {
      console.warn("Failed to access localStorage:", error);
    }

    // Scroll if URL has a hash
    const hash = window.location.hash;
    if (hash) {
      const el = document.querySelector(hash);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  useEffect(() => {
    if (zoneId) {
      localStorage.setItem("zoneId", zoneId);
      setZoneSelected(!!zoneId);
    }
  }, [zoneId]);

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-y-auto overflow-x-hidden">
        <div className="sticky top-0 z-10 bg-transparent lg:bg-blend-soft-light flex justify-end p-4">
          <ZoneDropdown selectedZoneId={zoneId} onChange={setZoneId} />
        </div>

        <div id="network-topology" className="h-screen mb-8 p-8">
          <h2 className="text-2xl font-bold mb-4">Network Topology</h2>
        </div>

        <div id="devices-overview" className="h-screen p-8">
          {zoneSelected && <DevicesOverview zoneId={zoneId} />}
        </div>
      </main>
    </div>
  );
}

export default Home;
