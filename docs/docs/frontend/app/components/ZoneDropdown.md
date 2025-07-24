[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/ZoneDropdown

# app/components/ZoneDropdown

## Functions

### ZoneDropdown()

> **ZoneDropdown**(`__namedParameters`): `Element`

Defined in: [app/components/ZoneDropdown.tsx:29](https://github.com/Abhi-MS/switchmap-ng/blob/541e84ce7b8b339a438f8adc6def2b02b4cae6cf/frontend/src/app/components/ZoneDropdown.tsx#L29)

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

 - Zone for the structure of a zone.
 - ZoneDropdownProps for the props used by the component.
 - useState for managing the selected zone state.
 - useEffect for fetching zones and handling side effects.
 - useRef for managing the dropdown reference to handle outside clicks.
