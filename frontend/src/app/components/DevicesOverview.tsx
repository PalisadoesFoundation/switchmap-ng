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
import { DeviceNode, InterfaceEdge } from "@/app/types/graphql/GetZoneDevices";
import { InterfaceNode } from "@/app/types/graphql/GetDeviceInterfaces";
import { formatUptime } from "@/app/utils/time";

/**
 * DevicesOverview component displays a table of devices with sorting, filtering, and pagination.
 *
 * @remarks
 * This component is designed for client-side use only because it relies on the `useState` and `useEffect` hooks
 * to manage state and handle side effects like data fetching. It also includes interactive elements like
 * search input and dropdowns that require client-side rendering.
 *
 * @returns The DevicesOverview component.
 *
 * @see {@link useEffect}, {@link useState} for React hooks used in the component.
 * @see {@link useReactTable} from `@tanstack/react-table` for table management.
 * @see {@link DevicesOverview} for the devices overview component itself.
 */

interface DevicesOverviewProps {
  devices: DeviceNode[];
  loading: boolean;
  error: string | null;
}

interface DeviceRow {
  id: string;
  name: string;
  hostname: string;
  ports: string;
  uptime: string;
  link: string;
}

const PAGE_SIZE = 10;

export function DevicesOverview({
  devices,
  loading,
  error,
}: DevicesOverviewProps) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [currentPage, setCurrentPage] = useState(1);

  const columnHelper = createColumnHelper<DeviceRow>();

  const columns = useMemo(
    () => [
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
      columnHelper.accessor("hostname", { header: "Hostname" }),
      columnHelper.accessor("ports", { header: "Active Ports" }),
      columnHelper.accessor("uptime", { header: "Uptime" }),
    ],
    [columnHelper]
  );

  const data = useMemo(() => {
    return devices.map((device) => {
      const interfaces = device.l1interfaces.edges.map(
        (e: InterfaceEdge) => e.node
      );
      const total = interfaces.length;
      const active = interfaces.filter(
        (p: InterfaceNode) => p.ifoperstatus === 1
      ).length;
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

  const table = useReactTable({
    data,
    columns,
    state: { sorting, globalFilter },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  const rows = table.getRowModel().rows;
  const totalPages = Math.ceil(rows.length / PAGE_SIZE);

  useEffect(() => {
    if (totalPages === 0) {
      if (currentPage !== 1) {
        setCurrentPage(1);
      }
      return;
    }
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [totalPages, currentPage]);

  const paginatedRows = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE;
    return rows.slice(start, start + PAGE_SIZE);
  }, [rows, currentPage]);

  if (loading) return <p>Loading devices...</p>;
  if (error) return <p>Error loading devices: {error}</p>;
  if (!devices.length) return <p>No devices found.</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Devices Overview</h2>

      <input
        value={globalFilter}
        onChange={(e) => {
          setGlobalFilter(e.target.value);
          setCurrentPage(1);
        }}
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
                    className="cursor-pointer px-4 py-2"
                  >
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                    <span className="float-right text-[0.5rem]">
                      {header.column.getIsSorted() === "asc" ? "⯅" : ""}
                      {header.column.getIsSorted() === "desc" ? "⯆" : ""}
                    </span>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {paginatedRows.length ? (
              paginatedRows.map((row) => (
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
            ) : (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-4 py-2 text-center text-gray-400"
                >
                  No data
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-4 mt-4">
          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => p - 1)}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm">
            Page {currentPage} of {totalPages}
          </span>
          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => p + 1)}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
      <h3 className="text-sm font-semibold mt-16 mb-2">
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
