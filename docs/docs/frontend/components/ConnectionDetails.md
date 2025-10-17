[**frontend**](../README.md)

***

[frontend](../modules.md) / components/ConnectionDetails

# components/ConnectionDetails

## Functions

### ConnectionDetails()

> **ConnectionDetails**(`device`): `Element`

Defined in: [components/ConnectionDetails.tsx:25](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/components/ConnectionDetails.tsx#L25)

ConnectionDetails component displays detailed information about a device's network interfaces.

#### Parameters

##### device

The device object containing interface details.

###### device

[`DeviceNode`](../types/graphql/GetZoneDevices.md#devicenode)

#### Returns

`Element`

The ConnectionDetails component.

#### Remarks

This component is designed to show the list of network interfaces for a specific device,
including their status, speed, and other relevant details. It allows users to view and
manage the network connections of the device.

#### See

 - [useState](#), useMemo, useCallback for React hooks used in the component.
 - [DeviceNode](../types/graphql/GetZoneDevices.md#devicenode), [InterfaceNode](../types/graphql/GetDeviceInterfaces.md#interfacenode), [MacPort](../types/graphql/GetDeviceInterfaces.md#macport) for the types used in the component.
