[**frontend**](../../README.md)

***

[frontend](../../modules.md) / types/graphql/GetDeviceInterfaces

# types/graphql/GetDeviceInterfaces

## Type Aliases

### GetDeviceInterfacesData

> **GetDeviceInterfacesData** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:83](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L83)

#### Properties

##### data

> **data**: `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:84](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L84)

###### device

> **device**: `object`

###### device.l1interfaces

> **l1interfaces**: [`L1Interfaces`](#l1interfaces)

##### errors?

> `optional` **errors**: `object`[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:89](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L89)

###### message

> **message**: `string`

***

### GetDeviceInterfacesVars

> **GetDeviceInterfacesVars** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:92](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L92)

#### Properties

##### id

> **id**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:93](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L93)

***

### InterfaceEdge

> **InterfaceEdge** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:75](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L75)

#### Properties

##### node

> **node**: [`InterfaceNode`](#interfacenode)

Defined in: [types/graphql/GetDeviceInterfaces.ts:76](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L76)

***

### InterfaceNode

> **InterfaceNode** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:44](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L44)

#### Properties

##### cdpcachedeviceid?

> `optional` **cdpcachedeviceid**: `string` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:65](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L65)

##### cdpcachedeviceport

> **cdpcachedeviceport**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:66](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L66)

##### cdpcacheplatform

> **cdpcacheplatform**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:67](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L67)

##### duplex

> **duplex**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:62](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L62)

##### idxDevice

> **idxDevice**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:46](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L46)

##### idxL1interface

> **idxL1interface**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:45](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L45)

##### ifalias?

> `optional` **ifalias**: `string` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:63](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L63)

##### ifinDiscards

> **ifinDiscards**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:60](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L60)

##### ifinErrors

> **ifinErrors**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:58](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L58)

##### ifinNUcastPkts

> **ifinNUcastPkts**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:54](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L54)

##### ifinOctets

> **ifinOctets**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:56](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L56)

##### ifinUcastPkts

> **ifinUcastPkts**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:52](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L52)

##### ifname

> **ifname**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:47](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L47)

##### ifoperstatus

> **ifoperstatus**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:49](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L49)

##### ifoutDiscards

> **ifoutDiscards**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:61](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L61)

##### ifoutErrors

> **ifoutErrors**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:59](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L59)

##### ifoutNUcastPkts

> **ifoutNUcastPkts**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:55](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L55)

##### ifoutOctets

> **ifoutOctets**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:57](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L57)

##### ifoutUcastPkts

> **ifoutUcastPkts**: `number` \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:53](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L53)

##### ifspeed

> **ifspeed**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:51](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L51)

##### lldpremportdesc

> **lldpremportdesc**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:68](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L68)

##### lldpremsyscapenabled

> **lldpremsyscapenabled**: `string`[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:71](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L71)

##### lldpremsysdesc

> **lldpremsysdesc**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:70](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L70)

##### lldpremsysname

> **lldpremsysname**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:69](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L69)

##### macports

> **macports**: [`MacPort`](#macport)

Defined in: [types/graphql/GetDeviceInterfaces.ts:72](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L72)

##### nativevlan

> **nativevlan**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:48](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L48)

##### trunk

> **trunk**: `boolean`

Defined in: [types/graphql/GetDeviceInterfaces.ts:64](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L64)

##### tsIdle

> **tsIdle**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:50](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L50)

***

### L1Interfaces

> **L1Interfaces** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:79](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L79)

#### Properties

##### edges

> **edges**: [`InterfaceEdge`](#interfaceedge)[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:80](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L80)

***

### Mac

> **Mac** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:27](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L27)

#### Properties

##### mac

> **mac**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:28](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L28)

##### oui

> **oui**: [`OrganizationOui`](#organizationoui) \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:29](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L29)

***

### MacPort

> **MacPort** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:40](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L40)

#### Properties

##### edges

> **edges**: [`MacsEdge`](#macsedge)[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:41](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L41)

***

### MacsEdge

> **MacsEdge** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:36](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L36)

#### Properties

##### node

> **node**: [`MacsNode`](#macsnode)

Defined in: [types/graphql/GetDeviceInterfaces.ts:37](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L37)

***

### MacsNode

> **MacsNode** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:32](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L32)

#### Properties

##### macs

> **macs**: [`Mac`](#mac)[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:33](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L33)

***

### OrganizationOui

> **OrganizationOui** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:23](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L23)

Type definitions for GraphQL queries related to device interfaces.
These types are used to structure the data returned from the GraphQL API.
They include definitions for MAC addresses, OUI (Organizationally Unique Identifier),
and device interfaces.

#### Remarks

This file defines the types used in the GraphQL queries for fetching device interfaces.
It includes types for MAC addresses, OUI, and the structure of device interfaces.
The types are used to ensure type safety when working with the data returned from the API.
The `Oui` type represents the organization associated with a MAC address,
while the `Mac` type represents a MAC address and its associated OUI.
The `MacsNode` type represents a collection of MAC addresses,
and the `MacPorts` type represents the edges of MAC addresses.
The `InterfaceNode` type represents a device interface with various properties,
including its name, status, speed, and associated MAC addresses.
The `InterfaceEdge` type represents an edge in the list of interfaces,
and the `L1Interfaces` type represents a collection of these edges.
Finally, the `GetDeviceInterfacesData` type represents the overall structure of the data returned
from the GraphQL query for device interfaces, including any potential errors.
The `GetDeviceInterfacesVars` type defines the variables required for the GraphQL query,
specifically the device ID.

#### Properties

##### organization

> **organization**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:24](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/types/graphql/GetDeviceInterfaces.ts#L24)
