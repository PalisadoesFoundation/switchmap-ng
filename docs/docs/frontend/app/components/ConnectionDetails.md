[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/ConnectionDetails

# app/components/ConnectionDetails

## Functions

### ConnectionDetails()

> **ConnectionDetails**(`deviceId`): `null` \| `Element`

Defined in: [app/components/ConnectionDetails.tsx:79](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/app/components/ConnectionDetails.tsx#L79)

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
 - QUERY for the GraphQL query used to fetch device interfaces.
 - InterfaceEdge and InterfaceNode for the structure of interface data.
 - MacPorts and MacsEdge for the structure of MAC address data.
 - extractMacAddresses and extractManufacturers for helper functions to process MAC data.
 - DeviceNode for the structure of the device node.
