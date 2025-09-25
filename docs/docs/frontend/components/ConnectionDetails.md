[**frontend**](../README.md)

***

[frontend](../modules.md) / components/ConnectionDetails

# components/ConnectionDetails

## Functions

### ConnectionDetails()

> **ConnectionDetails**(`deviceId`): `Element`

Defined in: [components/ConnectionDetails.tsx:29](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/components/ConnectionDetails.tsx#L29)

ConnectionDetails component fetches and displays detailed information about a device's interfaces.
It includes MAC addresses, manufacturers, and other relevant data.

#### Parameters

##### deviceId

The ID of the device to fetch details for. If not provided, it will use the ID from URL params.

###### device

[`DeviceNode`](../types/graphql/GetZoneDevices.md#devicenode)

#### Returns

`Element`

The rendered connection details table or an error message if data is unavailable.

#### Remarks

This component is designed for client-side use only because it relies on the `useParams` hook
to retrieve the device ID from the URL. It also handles loading and error states.

#### See

 - useParams for retrieving the device ID from URL parameters.
 - DeviceResponse for the structure of the device data.
 - QUERY for the GraphQL query used to fetch device details.
 - [InterfaceEdge](../types/graphql/GetDeviceInterfaces.md#interfaceedge) and [InterfaceNode](../types/graphql/GetDeviceInterfaces.md#interfacenode) for the structure of interface data.
 - [Mac](../types/graphql/GetDeviceInterfaces.md#mac) and [MacPort](../types/graphql/GetDeviceInterfaces.md#macport) for the structure of MAC address data.
