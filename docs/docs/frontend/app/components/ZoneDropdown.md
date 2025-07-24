[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/ZoneDropdown

# app/components/ZoneDropdown

## Functions

### ZoneDropdown()

> **ZoneDropdown**(`__namedParameters`): `Element`

Defined in: [app/components/ZoneDropdown.tsx:28](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/app/components/ZoneDropdown.tsx#L28)

ZoneDropdown component allows users to select a zone from a dropdown list.
It fetches the available zones from the API and manages the selected zone state.

#### Parameters

##### \_\_namedParameters

`ZoneDropdownProps`

#### Returns

`Element`

The rendered component.

#### Remarks

This component is designed for client-side use only because it relies on
the `useEffect` hook for fetching data and managing state.
It also handles click events outside the dropdown to close it.

#### See

 - Zone for the structure of zone data.
 - useEffect for fetching zones from the API.
 - useState for managing the dropdown state.
 - useRef for handling click outside events.
