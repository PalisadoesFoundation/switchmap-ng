[**frontend**](../README.md)

***

[frontend](../modules.md) / utils/deviceUtils

# utils/deviceUtils

## Type Aliases

### DeviceNode

> **DeviceNode** = `object`

Defined in: [utils/deviceUtils.ts:14](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/deviceUtils.ts#L14)

Utility functions for device management, including date parsing and filtering.

#### Remarks

This module provides functions to parse date strings and filter devices based on their last polled time.
It includes a type definition for device nodes used in the application.

#### See

 - [DeviceNode](#devicenode) for the device node structure.
 - [parseDateOnlyLocal](#parsedateonlylocal) for parsing date strings.
 - [filterDevicesByTimeRange](#filterdevicesbytimerange) for filtering devices by time range.

#### Properties

##### hostname

> **hostname**: `string`

Defined in: [utils/deviceUtils.ts:15](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/deviceUtils.ts#L15)

##### lastPolledMs?

> `optional` **lastPolledMs**: `number` \| `null`

Defined in: [utils/deviceUtils.ts:16](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/deviceUtils.ts#L16)

## Functions

### filterDevicesByTimeRange()

> **filterDevicesByTimeRange**(`devices`, `timeRange`, `start?`, `end?`): [`DeviceNode`](#devicenode)[]

Defined in: [utils/deviceUtils.ts:26](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/deviceUtils.ts#L26)

Filters devices by time range

#### Parameters

##### devices

[`DeviceNode`](#devicenode)[]

##### timeRange

`string`

##### start?

`string`

##### end?

`string`

#### Returns

[`DeviceNode`](#devicenode)[]

***

### parseDateOnlyLocal()

> **parseDateOnlyLocal**(`yyyyMmDd`): `Date`

Defined in: [utils/deviceUtils.ts:20](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/deviceUtils.ts#L20)

Parses a YYYY-MM-DD string to a local Date

#### Parameters

##### yyyyMmDd

`string`

#### Returns

`Date`
