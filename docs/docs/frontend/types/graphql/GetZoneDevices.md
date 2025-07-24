[**frontend**](../../README.md)

***

[frontend](../../modules.md) / types/graphql/GetZoneDevices

# types/graphql/GetZoneDevices

## Type Aliases

### DeviceEdge

> **DeviceEdge** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:49](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L49)

#### Properties

##### node

> **node**: [`DeviceNode`](#devicenode)

Defined in: [types/graphql/GetZoneDevices.ts:50](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L50)

***

### DeviceNode

> **DeviceNode** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:38](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L38)

#### Properties

##### hostname

> **hostname**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:45](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L45)

##### id

> **id**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:40](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L40)

##### idxDevice

> **idxDevice**: `number`

Defined in: [types/graphql/GetZoneDevices.ts:41](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L41)

##### l1interfaces

> **l1interfaces**: [`L1Interfaces`](#l1interfaces-1)

Defined in: [types/graphql/GetZoneDevices.ts:46](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L46)

##### sysDescription

> **sysDescription**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:39](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L39)

##### sysName

> **sysName**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:44](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L44)

##### sysObjectid

> **sysObjectid**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:42](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L42)

##### sysUptime

> **sysUptime**: `number`

Defined in: [types/graphql/GetZoneDevices.ts:43](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L43)

***

### Devices

> **Devices** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:60](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L60)

#### Properties

##### edges

> **edges**: [`DeviceEdge`](#deviceedge)[]

Defined in: [types/graphql/GetZoneDevices.ts:61](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L61)

***

### GetZoneDevicesData

> **GetZoneDevicesData** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:73](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L73)

#### Properties

##### data

> **data**: `object`

Defined in: [types/graphql/GetZoneDevices.ts:74](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L74)

###### zone

> **zone**: [`Zone`](#zone)

##### errors?

> `optional` **errors**: `object`[]

Defined in: [types/graphql/GetZoneDevices.ts:77](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L77)

###### message

> **message**: `string`

***

### GetZoneDevicesVars

> **GetZoneDevicesVars** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:80](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L80)

#### Properties

##### id

> **id**: `string`

Defined in: [types/graphql/GetZoneDevices.ts:81](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L81)

***

### InterfaceEdge

> **InterfaceEdge** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:30](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L30)

This file defines the types used in the GraphQL query for fetching devices in a zone.
It includes types for devices, interfaces, and their relationships. 
These types are used to ensure type safety when working with the data returned from the API.
The `DeviceNode` type represents a device with various properties, including its description, ID
and interfaces.
The `InterfaceNode` type represents a device interface with various properties,
including its name, status, speed, and associated MAC addresses.
The `InterfaceEdge` type represents an edge in the list of interfaces,
and the `L1Interfaces` type represents a collection of these edges.
The `DeviceEdge` type represents an edge in the list of devices,
and the `Devices` type represents a collection of these edges.
The `ZoneNode` type represents a zone containing devices,
and the `ZoneEdge` type represents an edge in the list of zones.
The `Zones` type represents a collection of zones.
The `GetZoneDevicesData` type represents the overall structure of the data returned
from the GraphQL query for zone devices, including any potential errors.
The `GetZoneDevicesVars` type defines the variables required for the GraphQL query,
specifically the zone ID.

#### Remarks

This file is part of the Switchmap-NG project, a modern network monitoring and analysis tool.
It is designed to provide a type-safe interface for working with GraphQL data in TypeScript.
The types defined here are used throughout the application to ensure that the data structures
are consistent and correctly typed, reducing the risk of runtime errors
and improving developer experience.

#### See

[InterfaceNode](GetDeviceInterfaces.md#interfacenode) for the structure of a device interface.

#### Properties

##### node

> **node**: [`InterfaceNode`](GetDeviceInterfaces.md#interfacenode)

Defined in: [types/graphql/GetZoneDevices.ts:31](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L31)

***

### L1Interfaces

> **L1Interfaces** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:34](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L34)

#### Properties

##### edges

> **edges**: [`InterfaceEdge`](#interfaceedge)[]

Defined in: [types/graphql/GetZoneDevices.ts:35](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L35)

***

### Zone

> **Zone** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:68](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L68)

#### Properties

##### devices

> **devices**: [`Devices`](#devices)

Defined in: [types/graphql/GetZoneDevices.ts:69](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L69)

***

### ZoneEdge

> **ZoneEdge** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:56](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L56)

#### Properties

##### node

> **node**: [`ZoneNode`](#zonenode)

Defined in: [types/graphql/GetZoneDevices.ts:57](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L57)

***

### ZoneNode

> **ZoneNode** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:52](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L52)

#### Properties

##### devices

> **devices**: [`Devices`](#devices)

Defined in: [types/graphql/GetZoneDevices.ts:53](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L53)

***

### Zones

> **Zones** = `object`

Defined in: [types/graphql/GetZoneDevices.ts:64](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L64)

#### Properties

##### edges

> **edges**: [`ZoneEdge`](#zoneedge)[]

Defined in: [types/graphql/GetZoneDevices.ts:65](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/types/graphql/GetZoneDevices.ts#L65)
