import { InterfaceNode } from "./GetDeviceInterfaces";
/**
 * This file defines the types used in the GraphQL query for fetching devices in a zone.
 * It includes types for devices, interfaces, and their relationships. 
 * These types are used to ensure type safety when working with the data returned from the API.
 * The `DeviceNode` type represents a device with various properties, including its description, ID
 * and interfaces.
 * The `InterfaceNode` type represents a device interface with various properties,
 * including its name, status, speed, and associated MAC addresses.
 * The `InterfaceEdge` type represents an edge in the list of interfaces,
 * and the `L1Interfaces` type represents a collection of these edges.
 * The `DeviceEdge` type represents an edge in the list of devices,
 * and the `Devices` type represents a collection of these edges.
 * The `ZoneNode` type represents a zone containing devices,
 * and the `ZoneEdge` type represents an edge in the list of zones.
 * The `Zones` type represents a collection of zones.
 * The `GetZoneDevicesData` type represents the overall structure of the data returned
 * from the GraphQL query for zone devices, including any potential errors.
 * The `GetZoneDevicesVars` type defines the variables required for the GraphQL query,
 * specifically the zone ID.
 * @remarks
 * This file is part of the Switchmap-NG project, a modern network monitoring and analysis tool.
 * It is designed to provide a type-safe interface for working with GraphQL data in TypeScript.
 * The types defined here are used throughout the application to ensure that the data structures
 * are consistent and correctly typed, reducing the risk of runtime errors
 * and improving developer experience.
 * @see {@link InterfaceNode} for the structure of a device interface.
 */

export type InterfaceEdge = {
  node: InterfaceNode;
};

export type L1Interfaces = {
  edges: InterfaceEdge[];
};

export type DeviceNode = {
  sysDescription: string;
  id: string;
  idxDevice: number;
  sysObjectid: string;
  sysUptime: number;
  sysName: string;
  hostname: string;
  l1interfaces: L1Interfaces;
  lastPolled: number | null;
};

export type DeviceEdge = {
  node: DeviceNode;
};
export type ZoneNode = {
  devices: Devices;
};

export type ZoneEdge = {
  node: ZoneNode;
};

export type Devices = {
  edges: DeviceEdge[];
};

export type Zones = {
  edges: ZoneEdge[];
};

export type Zone = {
  devices: Devices;
};


export type GetZoneDevicesData = {
  data: {
    zone: Zone;
  };
  errors?: { message: string }[];
};

export type GetZoneDevicesVars = {
  id: string;
};

