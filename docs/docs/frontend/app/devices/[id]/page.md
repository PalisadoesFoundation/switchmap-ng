[**frontend**](../../../README.md)

***

[frontend](../../../modules.md) / app/devices/\[id\]/page

# app/devices/\[id\]/page

## Functions

### DevicePage()

> **DevicePage**(): `Element`

Defined in: [app/devices/\[id\]/page.tsx:27](https://github.com/Abhi-MS/switchmap-ng/blob/0b476abc2d57c1ee976a5c61d2c9e2070484df73/frontend/src/app/devices/[id]/page.tsx#L27)

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
