[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/ConnectionDetails

# app/components/ConnectionDetails

## Functions

### ConnectionDetails()

> **ConnectionDetails**(`deviceId`): `null` \| `Element`

Defined in: [app/components/ConnectionDetails.tsx:77](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/components/ConnectionDetails.tsx#L77)

ConnectionDetails component fetches and displays detailed information about a device's interfaces.
It includes MAC addresses, manufacturers, and other relevant data.

#### Parameters

##### deviceId

The ID of the device to fetch details for. If not provided, it will use the ID from URL params.

###### deviceId?

`string`

#### Returns

`null` \| `Element`

The rendered connection details table or an error message if data is unavailable.

#### Remarks

This component is designed for client-side use only because it relies on the `useParams` hook
to retrieve the device ID from the URL. It also handles loading and error states.

#### See

 - useParams for retrieving the device ID from URL parameters.
 - DeviceResponse for the structure of the device data.
 - QUERY for the GraphQL query used to fetch device details.
 - [InterfaceEdge](../../types/graphql/GetDeviceInterfaces.md#interfaceedge) and [InterfaceNode](../../types/graphql/GetDeviceInterfaces.md#interfacenode) for the structure of interface data.
 - [Mac](../../types/graphql/GetDeviceInterfaces.md#mac) and [MacPorts](../../types/graphql/GetDeviceInterfaces.md#macports-1) for handling MAC address data.
