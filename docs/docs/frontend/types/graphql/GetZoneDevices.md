[**frontend**](../../README.md)

***

[frontend](../../modules.md) / types/graphql/GetZoneDevices

# types/graphql/GetZoneDevices

## Type Aliases

### DeviceEdge

> **DeviceEdge** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:22](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L22)

#### Properties

##### node

> **node**: [`DeviceNode`](#devicenode)

Defined in: [types/graphql/GetZoneDevices.ts:23](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L23)

***

### DeviceNode

> **DeviceNode** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:11](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L11)

#### Properties

##### hostname

> **hostname**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:18](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L18)

##### id

> **id**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:13](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L13)

##### idxDevice

> **idxDevice**: `number`

Defined in: [types/graphql/GetZoneDevices.ts:14](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L14)

##### l1interfaces

> **l1interfaces**: [`L1Interfaces`](#l1interfaces-1)

Defined in: [types/graphql/GetZoneDevices.ts:19](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L19)

##### sysDescription

> **sysDescription**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:12](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L12)

##### sysName

> **sysName**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:17](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L17)

##### sysObjectid

> **sysObjectid**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:15](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L15)

##### sysUptime

> **sysUptime**: `number`

Defined in: [types/graphql/GetZoneDevices.ts:16](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L16)

***

### Devices

> **Devices** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:33](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L33)

#### Properties

##### edges

> **edges**: [`DeviceEdge`](#deviceedge)[]

Defined in: [types/graphql/GetZoneDevices.ts:34](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L34)

***

### GetZoneDevicesData

> **GetZoneDevicesData** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:46](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L46)

#### Properties

##### data

> **data**: `object`

Defined in: [types/graphql/GetZoneDevices.ts:47](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L47)

###### zone

> **zone**: [`Zone`](#zone)

##### errors?

> `optional` **errors**: `object`[]

Defined in: [types/graphql/GetZoneDevices.ts:50](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L50)

###### message

> **message**: `string`

***

### GetZoneDevicesVars

> **GetZoneDevicesVars** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:53](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L53)

#### Properties

##### id

> **id**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:54](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L54)

***

### InterfaceEdge

> **InterfaceEdge** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:3](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L3)

#### Properties

##### node

> **node**: [`InterfaceNode`](GetDeviceInterfaces.md#interfacenode)

Defined in: [types/graphql/GetZoneDevices.ts:4](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L4)

***

### L1Interfaces

> **L1Interfaces** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:7](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L7)

#### Properties

##### edges

> **edges**: [`InterfaceEdge`](#interfaceedge)[]

Defined in: [types/graphql/GetZoneDevices.ts:8](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L8)

***

### Zone

> **Zone** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:41](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L41)

#### Properties

##### devices

> **devices**: [`Devices`](#devices)

Defined in: [types/graphql/GetZoneDevices.ts:42](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L42)

***

### ZoneEdge

> **ZoneEdge** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:29](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L29)

#### Properties

##### node

> **node**: [`ZoneNode`](#zonenode)

Defined in: [types/graphql/GetZoneDevices.ts:30](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L30)

***

### ZoneNode

> **ZoneNode** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:25](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L25)

#### Properties

##### devices

> **devices**: [`Devices`](#devices)

Defined in: [types/graphql/GetZoneDevices.ts:26](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L26)

***

### Zones

> **Zones** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:37](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L37)

#### Properties

##### edges

> **edges**: [`ZoneEdge`](#zoneedge)[]

Defined in: [types/graphql/GetZoneDevices.ts:38](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/types/graphql/GetZoneDevices.ts#L38)
