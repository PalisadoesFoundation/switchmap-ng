"use client";
import { useState, useMemo, useCallback } from "react";
import { DeviceNode } from "@/app/types/graphql/GetZoneDevices";
import {
  InterfaceEdge,
  InterfaceNode,
  MacPort,
} from "@/app/types/graphql/GetDeviceInterfaces";

export function ConnectionDetails({ device }: { device: DeviceNode }) {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 15;

  const interfaces = useMemo(
    () =>
      device.l1interfaces?.edges
        ?.map(({ node }: InterfaceEdge) => node)
        .filter(Boolean) ?? [],
    [device.l1interfaces]
  );

  const totalPages = Math.ceil(interfaces.length / itemsPerPage);

  const paginatedInterfaces = useMemo(
    () =>
      interfaces.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
      ),
    [interfaces, currentPage]
  );

  const extractMacAddresses = useCallback((macports?: MacPort) => {
    if (!Array.isArray(macports?.edges) || macports.edges.length === 0)
      return "";
    return macports.edges
      .flatMap((edge) => {
        const macs = edge?.node?.macs;
        const macList = Array.isArray(macs) ? macs : macs ? [macs] : [];
        return macList.map((macObj) => macObj?.mac).filter(Boolean);
      })
      .join(", ");
  }, []);

  const extractManufacturers = useCallback((macports?: MacPort) => {
    if (!Array.isArray(macports?.edges) || macports.edges.length === 0)
      return "";
    return macports.edges
      .flatMap((edge) => {
        const macs = edge?.node?.macs;
        const macList = Array.isArray(macs) ? macs : macs ? [macs] : [];
        return macList
          .map((macObj) => macObj?.oui?.organization)
          .filter(Boolean);
      })
      .join(", ");
  }, []);

  const getStatusText = (status?: number) =>
    status === 1 ? "Active" : status === 2 ? "Disabled" : "N/A";

  const getStatusBg = (status?: number) =>
    status === 1
      ? "bg-[#0072B2]/10 dark:bg-[#56B4E9]/10"
      : status === 2
      ? "bg-[#E69F00]/10 dark:bg-[#F0E442]/10"
      : "bg-gray-100/10 dark:bg-gray-700/10";

  if (!interfaces.length) return <p>No interface data available.</p>;

  const InterfaceRow = ({ iface }: { iface: InterfaceNode }) => (
    <tr
      className={`${getStatusBg(
        iface.ifoperstatus
      )} transition-colors duration-300`}
    >
      <td>{iface.ifname || "N/A"}</td>
      <td>{iface.nativevlan ?? "N/A"}</td>
      <td>{getStatusText(iface.ifoperstatus)}</td>
      <td>{iface.tsIdle ?? "N/A"}</td>
      <td>{iface.ifspeed ?? "N/A"}</td>
      <td>{iface.duplex ?? "N/A"}</td>
      <td>{iface.ifalias || "N/A"}</td>
      <td>{iface.trunk ? "Trunk" : "-"}</td>
      <td>
        {iface.cdpcachedeviceid ? (
          <div>
            {iface.cdpcachedeviceid}
            <div>{iface.cdpcachedeviceport}</div>
          </div>
        ) : (
          "-"
        )}
      </td>
      <td>
        {iface.lldpremsysname ? (
          <div>
            {iface.lldpremsysname}
            <div>{iface.lldpremportdesc}</div>
          </div>
        ) : (
          "-"
        )}
      </td>
      <td>{extractMacAddresses(iface.macports)}</td>
      <td>{extractManufacturers(iface.macports)}</td>
      <td></td>
      <td></td>
    </tr>
  );

  return (
    <div className="p-8 w-[80vw] flex flex-col gap-4 h-full">
      <h2 className="text-xl font-semibold mb-2">Connection Details</h2>
      <div className="w-full h-full overflow-auto rounded-lg">
        <table className="w-full h-full border border-border rounded-lg shadow-sm">
          <thead>
            <tr className="sticky top-0 bg-bg z-10">
              {[
                "Port",
                "VLAN",
                "State",
                "Days Inactive",
                "Speed",
                "Duplex",
                "Port Label",
                "Trunk",
                "CDP",
                "LLDP",
                "Mac Address",
                "Manufacturer",
                "IP Address",
                "DNS Name",
              ].map((title) => (
                <th key={title}>{title}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedInterfaces.map((iface) => (
              <InterfaceRow
                key={iface.idxDevice + iface.ifname}
                iface={iface}
              />
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination controls */}
      <div className="flex justify-center gap-2 mt-4">
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          className="px-3 py-1 border rounded disabled:opacity-50"
        >
          Prev
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
          className="px-3 py-1 border rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
