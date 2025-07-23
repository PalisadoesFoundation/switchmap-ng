export type Oui = {
  organization: string;
};

export type Mac = {
  mac: string;
  oui: Oui | null;
};

export type MacsNode = {
  macs: Mac[];
};

export type MacsEdge = {
  node: MacsNode;
};

export type MacPorts = {
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
  ifalias: string;
  trunk: boolean;
  cdpcachedeviceid: string;
  cdpcachedeviceport: string;
  cdpcacheplatform: string;
  lldpremportdesc: string;
  lldpremsysname: string;
  lldpremsysdesc: string;
  lldpremsyscapenabled: string[];
  macports: MacPorts;
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
