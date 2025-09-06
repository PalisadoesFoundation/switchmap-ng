/** 
 * Type definitions for GraphQL queries related to device interfaces.
 * These types are used to structure the data returned from the GraphQL API.
 * They include definitions for MAC addresses, OUI (Organizationally Unique Identifier),
 * and device interfaces.
 * @remarks
 * This file defines the types used in the GraphQL queries for fetching device interfaces.
 * It includes types for MAC addresses, OUI, and the structure of device interfaces.
 * The types are used to ensure type safety when working with the data returned from the API.
 * The `Oui` type represents the organization associated with a MAC address,
 * while the `Mac` type represents a MAC address and its associated OUI.
 * The `MacsNode` type represents a collection of MAC addresses,
 * and the `MacPorts` type represents the edges of MAC addresses.
 * The `InterfaceNode` type represents a device interface with various properties,
 * including its name, status, speed, and associated MAC addresses.
 * The `InterfaceEdge` type represents an edge in the list of interfaces,
 * and the `L1Interfaces` type represents a collection of these edges.
 * Finally, the `GetDeviceInterfacesData` type represents the overall structure of the data returned
 * from the GraphQL query for device interfaces, including any potential errors.
 * The `GetDeviceInterfacesVars` type defines the variables required for the GraphQL query,
 * specifically the device ID.
 */
export type OrganizationOui = {
  organization: string;
};

export type Mac = {
  mac: string;
  oui: OrganizationOui | null;
};

export type MacsNode = {
  macs: Mac[];
};

export type MacsEdge = {
  node: MacsNode;
};

export type MacPort = {
  edges: MacsEdge[];
};

export type InterfaceNode = {  
  idxL1interface: string;  
  idxDevice: number;  
  ifname: string;  
  nativevlan: number;  
  ifoperstatus: number;  
  tsIdle: string;  
  ifspeed: number;  
  duplex: string;  
  ifalias?: string | null;  
  trunk: boolean;  
  cdpcachedeviceid?: string | null;  
  cdpcachedeviceport: string;  
  cdpcacheplatform: string;  
  lldpremportdesc: string;  
  lldpremsysname: string;  
  lldpremsysdesc: string;  
  lldpremsyscapenabled: string[];  
  macports: MacPort;  
};  

export type InterfaceEdge = {
  node: InterfaceNode;
};

export type L1Interfaces = {
  edges: InterfaceEdge[];
};

export type GetDeviceInterfacesData = {
  data: {
    device: {
      l1interfaces: L1Interfaces;
    };
  };
  errors?: { message: string }[];
};

export type GetDeviceInterfacesVars = {
  id: string;
};
