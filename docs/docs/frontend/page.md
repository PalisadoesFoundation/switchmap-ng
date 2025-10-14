[**frontend**](README.md)

***

[frontend](modules.md) / page

# page

## Variables

### \_testUtils

> `const` **\_testUtils**: `object`

Defined in: [page.tsx:340](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/page.tsx#L340)

#### Type declaration

##### clearDeviceCache()

> **clearDeviceCache**: () => `void`

###### Returns

`void`

## Functions

### default()

> **default**(): `Element`

Defined in: [page.tsx:55](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/page.tsx#L55)

Home page component displaying network topology and devices overview.

#### Returns

`Element`

The main home page component.

#### Remarks

This component fetches and displays devices based on the selected zone.
It includes a sidebar, a zone selection dropdown, a topology chart, and
a devices overview section. The component uses caching to minimize
unnecessary API calls and improve performance.

#### See

 - [Sidebar](components/Sidebar.md#sidebar) for the navigation sidebar.
 - [ZoneDropdown](components/ZoneDropdown.md#zonedropdown) for selecting network zones.
 - TopologyChart for visualizing network topology.
 - DevicesOverview for listing devices in a tabular format.
