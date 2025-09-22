[**frontend**](../README.md)

***

[frontend](../modules.md) / utils/timeStamp

# utils/timeStamp

## Functions

### formatUnixTimestamp()

> **formatUnixTimestamp**(`timestamp?`): `string`

Defined in: [utils/timeStamp.ts:7](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/timeStamp.ts#L7)

Converts a Unix timestamp (in seconds) to a human-readable date and time string.
If the timestamp is invalid or not provided, it returns "Unknown".

#### Parameters

##### timestamp?

The Unix timestamp in seconds (string or number).

`null` | `string` | `number`

#### Returns

`string`

A formatted date and time string or "Unknown".
