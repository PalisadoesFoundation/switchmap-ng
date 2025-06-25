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

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        setLoading(true);

        const res = await fetch("http://localhost:7000/switchmap/api/graphql", {
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
            variables: {
              id: zoneId,
            },
          }),
        });

        const json = await res.json();
        const rawDevices = json.data.zone.devices.edges.map(
          (edge: any) => edge.node
        );
        setDevices(rawDevices);
      } catch (err) {
        console.error("Error fetching devices:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, [zoneId]);

  const columnHelper = createColumnHelper<any>();

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

  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Devices Overview</h2>

      <input
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        placeholder="Search..."
        className="mb-4 p-2 border rounded w-full max-w-sm"
      />
      <h3 className="text-sm font-semibold mt-8 mb-2">
        DEVICES MONITORED BY SWITCHMAP
      </h3>
      <table className="w-full text-left border border-collapse">
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id} className="border-b">
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  className="cursor-pointer px-4 py-2 border"
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
          {table.getRowModel().rows.map((row) => (
            <tr
              key={row.id}
              className="border-b hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-2 border">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <h3 className="text-sm font-semibold mt-8 mb-2">
        DEVICES NOT MONITORED BY SWITCHMAP
      </h3>
      <table className="w-full text-left border border-collapse">
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id} className="border-b">
              {headerGroup.headers.map((header) => (
                <th key={header.id} className="px-4 py-2 border">
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
              className="px-4 py-2 border text-center text-gray-400"
            >
              No data
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
