[**frontend**](../README.md)

***

[frontend](../modules.md) / app/page

# app/page

## Functions

### Home()

> **Home**(): `Element`

Defined in: [app/page.tsx:28](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/page.tsx#L28)

Main entry point for the application.

This component renders the sidebar and main content area,
including the network topology and devices overview sections.
It also manages the selected zone state and persists it in localStorage.

#### Returns

`Element`

The rendered component.

#### Remarks

This component is the main page of the application.
It initializes the zone ID from localStorage and updates it
whenever the user selects a different zone.
It also handles scrolling to elements based on the URL hash.

#### See

 - [Sidebar](components/Sidebar.md#sidebar) for the sidebar component.
 - [ZoneDropdown](components/ZoneDropdown.md#zonedropdown) for the zone selection dropdown.
 - [DevicesOverview](components/DevicesOverview.md#devicesoverview) for displaying devices in the selected zone.
