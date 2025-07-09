export type InterfaceNode = {
  ifoperstatus: string;
  cdpcachedeviceid: string;
  cdpcachedeviceport: string;
};

export type InterfaceEdge = {
  node: InterfaceNode;
};

export type L1Interfaces = {
  edges: InterfaceEdge[];
};

export type DeviceNode = {
  idxDevice: number;
  sysObjectid: string;
  sysUptime: number;
  sysName: string;
  hostname: string;
  l1interfaces: L1Interfaces;
};

export type DeviceEdge = {
  node: DeviceNode;
};

export type Devices = {
  edges: DeviceEdge[];
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

