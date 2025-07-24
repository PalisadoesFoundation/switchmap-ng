[**frontend**](../README.md)

***

[frontend](../modules.md) / app/page

# app/page

## Functions

### Home()

> **Home**(): `Element`

Defined in: [app/page.tsx:28](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/app/page.tsx#L28)

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

 - Sidebar
 - DevicesOverview
 - ZoneDropdown
