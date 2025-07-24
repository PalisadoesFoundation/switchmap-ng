[**frontend**](../../../README.md)

***

[frontend](../../../modules.md) / app/devices/\[id\]/page

# app/devices/\[id\]/page

## Functions

### DevicePage()

> **DevicePage**(): `Element`

Defined in: [app/devices/\[id\]/page.tsx:27](https://github.com/Abhi-MS/switchmap-ng/blob/e3f3cee2a7bf54269767383c79698e3c0a861e46/frontend/src/app/devices/[id]/page.tsx#L27)

Renders the DevicePage component, showing detailed information about a specific device.

Includes a sidebar for navigation and tabbed sections for various device data,
such as overview, connection details, and connection charts.

#### Returns

`Element`

The rendered device detail page.

#### Remarks

- Designed for client-side rendering only, as it relies on `useParams` and `useSearchParams`.
- Uses a responsive layout that adjusts based on sidebar visibility.
- Handles active tab state and sidebar toggle logic.
- Icons from `react-icons` visually represent each tab.
- Includes a Home button for quick navigation.

#### See

 - [ConnectionDetails](../../components/ConnectionDetails.md#connectiondetails) for displaying device interface details.
 - [ThemeToggle](../../theme-toggle.md#themetoggle) for the theme switching functionality.
