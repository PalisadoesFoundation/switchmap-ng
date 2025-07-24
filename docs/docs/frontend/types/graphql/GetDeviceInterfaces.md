[**frontend**](../../README.md)

***

[frontend](../../modules.md) / types/graphql/GetDeviceInterfaces

# types/graphql/GetDeviceInterfaces

## Type Aliases

### GetDeviceInterfacesData

> **GetDeviceInterfacesData** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:51](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L51)

#### Properties

##### data

> **data**: `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:52](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L52)

###### device

> **device**: `object`

###### device.l1interfaces

> **l1interfaces**: [`L1Interfaces`](#l1interfaces)

##### errors?

> `optional` **errors**: `object`[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:57](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L57)

###### message

> **message**: `string`

***

### GetDeviceInterfacesVars

> **GetDeviceInterfacesVars** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:60](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L60)

#### Properties

##### id

> **id**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:61](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L61)

***

### InterfaceEdge

> **InterfaceEdge** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:43](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L43)

#### Properties

##### node

> **node**: [`InterfaceNode`](#interfacenode)

Defined in: [types/graphql/GetDeviceInterfaces.ts:44](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L44)

***

### InterfaceNode

> **InterfaceNode** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:22](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L22)

#### Properties

##### cdpcachedeviceid

> **cdpcachedeviceid**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:33](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L33)

##### cdpcachedeviceport

> **cdpcachedeviceport**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:34](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L34)

##### cdpcacheplatform

> **cdpcacheplatform**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:35](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L35)

##### duplex

> **duplex**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:30](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L30)

##### idxDevice

> **idxDevice**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:24](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L24)

##### idxL1interface

> **idxL1interface**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:23](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L23)

##### ifalias

> **ifalias**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:31](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L31)

##### ifname

> **ifname**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:25](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L25)

##### ifoperstatus

> **ifoperstatus**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:27](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L27)

##### ifspeed

> **ifspeed**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:29](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L29)

##### lldpremportdesc

> **lldpremportdesc**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:36](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L36)

##### lldpremsyscapenabled

> **lldpremsyscapenabled**: `string`[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:39](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L39)

##### lldpremsysdesc

> **lldpremsysdesc**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:38](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L38)

##### lldpremsysname

> **lldpremsysname**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:37](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L37)

##### macports

> **macports**: [`MacPorts`](#macports-1)

Defined in: [types/graphql/GetDeviceInterfaces.ts:40](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L40)

##### nativevlan

> **nativevlan**: `number`

Defined in: [types/graphql/GetDeviceInterfaces.ts:26](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L26)

##### trunk

> **trunk**: `boolean`

Defined in: [types/graphql/GetDeviceInterfaces.ts:32](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L32)

##### tsIdle

> **tsIdle**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:28](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L28)

***

### L1Interfaces

> **L1Interfaces** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:47](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L47)

#### Properties

##### edges

> **edges**: [`InterfaceEdge`](#interfaceedge)[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:48](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L48)

***

### Mac

> **Mac** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:5](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L5)

#### Properties

##### mac

> **mac**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:6](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L6)

##### oui

> **oui**: [`Oui`](#oui-1) \| `null`

Defined in: [types/graphql/GetDeviceInterfaces.ts:7](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L7)

***

### MacPorts

> **MacPorts** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:18](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L18)

#### Properties

##### edges

> **edges**: [`MacsEdge`](#macsedge)[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:19](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L19)

***

### MacsEdge

> **MacsEdge** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:14](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L14)

#### Properties

##### node

> **node**: [`MacsNode`](#macsnode)

Defined in: [types/graphql/GetDeviceInterfaces.ts:15](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L15)

***

### MacsNode

> **MacsNode** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:10](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L10)

#### Properties

##### macs

> **macs**: [`Mac`](#mac)[]

Defined in: [types/graphql/GetDeviceInterfaces.ts:11](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L11)

***

### Oui

> **Oui** = `object`

Defined in: [types/graphql/GetDeviceInterfaces.ts:1](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L1)

#### Properties

##### organization

> **organization**: `string`

Defined in: [types/graphql/GetDeviceInterfaces.ts:2](https://github.com/Abhi-MS/switchmap-ng/blob/9fe8d4a0f80ad32d2d4df5e7beea90d8b3d2deb3/frontend/src/types/graphql/GetDeviceInterfaces.ts#L2)
