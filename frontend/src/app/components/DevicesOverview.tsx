"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  flexRender,
  createColumnHelper,
  SortingState,
} from "@tanstack/react-table";

// Device type definition
type Device = {
  idxDevice: string;
  id: string;
  sysName: string | null;
  hostname: string | null;
  sysObjectid: string | null;
  sysUptime: number;
  l1interfaces: {
    edges: { node: { ifoperstatus: number } }[];
  };
};

// Format uptime from hundredths of seconds to readable string
const formatUptime = (hundredths: number) => {
  const seconds = Math.floor(hundredths / 100);
  const days = Math.floor(seconds / 86400);
  const hrs = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${days}d ${hrs}h ${mins}m ${secs}s`;
};

export default function DevicesOverview({ zoneId }: { zoneId: string }) {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!zoneId) {
      setDevices([]);
      setLoading(false);
      setError("Waiting for zone selection to load devices.");
      return;
    }
    const fetchDevices = async () => {
      try {
        setLoading(true);
        setError(null); // reset error before fetch

        const res = await fetch(
          process.env.NEXT_PUBLIC_API_URL ||
            "http://localhost:7000/switchmap/api/graphql",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              query: `
              query GetZoneDevices($id: ID!) {
                zone(id: $id) {
                  devices {
                    edges {
                      node {
                        idxDevice
                        sysObjectid
                        sysUptime
                        sysName
                        hostname
                        l1interfaces {
                          edges {
                            node {
                              ifoperstatus
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            `,
              variables: { id: zoneId },
            }),
          }
        );

        if (!res.ok) {
          throw new Error(`Network response was not ok: ${res.statusText}`);
        }

        const json = await res.json();

        if (json.errors) {
          throw new Error(json.errors.map((e: any) => e.message).join(", "));
        }

        const rawDevices =
          json.data?.zone?.devices?.edges?.map((edge: any) => edge.node) || [];
        setDevices(rawDevices);
      } catch (err: any) {
        console.error("Error fetching devices:", err?.message || err);
        setDevices([]); // clear old data
        setError(
          "Failed to load devices. Please check your network or try again."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, [zoneId]);

  const columnHelper = createColumnHelper<any>();

  // Prepare table data from devices
  const data = useMemo(() => {
    return devices.map((device) => {
      const interfaces = device.l1interfaces.edges.map((e) => e.node);
      const total = interfaces.length;
      const active = interfaces.filter((p) => p.ifoperstatus === 1).length;

      return {
        id: device.id,
        name: device.sysName || "-",
        hostname: device.hostname || "-",
        ports: `${active}/${total}`,
        uptime: formatUptime(device.sysUptime),
        link: `/devices/${encodeURIComponent(
          device.idxDevice ?? device.id
        )}?sysName=${encodeURIComponent(
          device.sysName ?? device.hostname ?? ""
        )}#devices-overview`,
      };
    });
  }, [devices]);

  // Table columns definition
  const columns = [
    columnHelper.accessor("name", {
      header: "Device Name",
      cell: (info) => (
        <Link
          href={info.row.original.link}
          className="text-blue-600 hover:underline"
        >
          {info.getValue()}
        </Link>
      ),
    }),
    columnHelper.accessor("hostname", {
      header: "Hostname",
    }),
    columnHelper.accessor("ports", {
      header: "Active Ports",
    }),
    columnHelper.accessor("uptime", {
      header: "Uptime",
    }),
  ];

  // Create table instance
  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      globalFilter,
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Devices Overview</h2>

      {/* Global search filter */}
      <input
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        placeholder="Search..."
        className="mb-4 p-2 border rounded w-full max-w-sm"
      />
      <h3 className="text-sm font-semibold mt-8 mb-2">
        DEVICES MONITORED BY SWITCHMAP
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left min-w-full">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr
                key={headerGroup.id}
                className="border-b border-bottom-border"
              >
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    onClick={header.column.getToggleSortingHandler()}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        header.column.getToggleSortingHandler()?.(e);
                      }
                    }}
                    className="cursor-pointer px-4 py-2"
                    tabIndex={0}
                    role="button"
                    aria-label={`Sort by ${header.column.columnDef.header}`}
                  >
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                    <span
                      className="float-right text-center text-[0.5rem] "
                      style={{ userSelect: "none" }}
                    >
                      <span
                        style={{ display: "block" }}
                        className={
                          header.column.getIsSorted() === "asc"
                            ? "text-blue-600"
                            : "text-gray-400"
                        }
                      >
                        ⯅
                      </span>
                      <span
                        style={{ display: "block" }}
                        className={
                          header.column.getIsSorted() === "desc"
                            ? "text-blue-600"
                            : "text-gray-400"
                        }
                      >
                        ⯆
                      </span>
                    </span>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-4 py-2 text-center text-gray-400"
                >
                  No data
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <tr key={row.id} className="hover:hover-bg">
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-2">
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <h3 className="text-sm font-semibold mt-8 mb-2">
        DEVICES NOT MONITORED BY SWITCHMAP
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left min-w-full">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="border-b border-gray-200">
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="px-4 py-2">
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            <tr>
              <td
                colSpan={columns.length}
                className="px-4 py-2 text-center text-gray-400"
              >
                No data
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
