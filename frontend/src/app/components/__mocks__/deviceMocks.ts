// __mocks__/deviceMocks.ts
import { InterfaceNode } from "@/app/types/graphql/GetDeviceInterfaces";
import { DeviceNode } from "../../types/graphql/GetZoneDevices";

const mockInterface: InterfaceNode = {
  idxL1interface: "1",
  idxDevice: 1,
  ifname: "Gig1/0/1",
  nativevlan: 10,
  ifoperstatus: 1,
  tsIdle: "100",
  ifspeed: 1000,
  duplex: "full",
  ifalias: "uplink",
  trunk: true,
  cdpcachedeviceid: "dev1",
  cdpcachedeviceport: "Gig1/0/2",
  cdpcacheplatform: "Cisco 9300",
  lldpremportdesc: "Gi1/0/1",
  lldpremsysname: "switch1",
  lldpremsysdesc: "Cisco 9300",
  lldpremsyscapenabled: ["R", "S"],
  macports: {
    edges: [
      {
        node: {
          macs: [{ mac: "00:11:22:33:44:55", oui: { organization: "Cisco" } }],
        },
      },
    ],
  },
};

export const mockDevice: DeviceNode = {
  id: "1",
  idxDevice: 1,
  hostname: "host1",
  sysName: "Device 1",
  sysDescription: "Test device description",
  sysObjectid: "1.3.6.1",
  sysUptime: 1000,
  lastPolled: 1693305600,
  l1interfaces: {
    edges: [{ node: mockInterface }],
  },
};


