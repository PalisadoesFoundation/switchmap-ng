// __mocks__/deviceMocks.ts
import { DeviceNode } from "../../types/graphql/GetZoneDevices";

export const mockDevice: DeviceNode = {
  id: "1",
  idxDevice: 1,
  hostname: "host1",
  sysName: "Device 1",
  sysDescription: "Test device description",
  sysObjectid: "1.3.6.1",
  sysUptime: 1000,
  lastPolled: "1693305600",
  l1interfaces: {
    edges: [], 
  },
};
