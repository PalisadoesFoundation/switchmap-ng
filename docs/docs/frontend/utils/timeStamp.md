[**frontend**](../README.md)

***

[frontend](../modules.md) / utils/timeStamp

# utils/timeStamp

## Functions

### formatUnixTimestamp()

> **formatUnixTimestamp**(`timestamp?`): `string`

Defined in: [utils/timeStamp.ts:12](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/utils/timeStamp.ts#L12)

Formats a Unix timestamp (in seconds) into a human-readable date and time string.

#### Parameters

##### timestamp?

The Unix timestamp in seconds. Can be a number or a string.

`null` | `string` | `number`

#### Returns

`string`

A formatted date and time string or "Unknown" for invalid inputs.

#### Remarks

If the timestamp is invalid, undefined, null, or non-positive, the function returns "Unknown".
Otherwise, it converts the timestamp to a Date object and formats it using the
user's local date and time settings.
