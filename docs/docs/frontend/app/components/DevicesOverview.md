[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/DevicesOverview

# app/components/DevicesOverview

## Functions

### DevicesOverview()

> **DevicesOverview**(`__namedParameters`): `Element`

Defined in: [app/components/DevicesOverview.tsx:64](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/components/DevicesOverview.tsx#L64)

DevicesOverview component fetches and displays a list of devices in a table format.
It supports sorting and filtering of device data.

#### Parameters

##### \_\_namedParameters

###### zoneId

`string`

#### Returns

`Element`

The rendered component.

#### Remarks

This component is designed for client-side use only because it relies on the `useEffect`
hook for fetching data and managing state.
It also uses the `useReactTable` hook from `@tanstack/react-table`
for table management.

#### See

 - Device for the structure of device data.
 - useEffect for fetching devices from the API.
 - useState for managing the component state.
 - useReactTable for table management.
 - formatUptime for converting uptime from hundredths of seconds to a readable string.
 - createColumnHelper for creating table columns.
 - SortingState for managing sorting state in the table.
 - getCoreRowModel, getFilteredRowModel, getSortedRowModel for table row models.
