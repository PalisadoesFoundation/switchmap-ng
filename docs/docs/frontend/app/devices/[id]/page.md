[**frontend**](../../../README.md)

***

[frontend](../../../modules.md) / app/devices/\[id\]/page

# app/devices/\[id\]/page

## Functions

### DevicePage()

> **DevicePage**(): `Element`

Defined in: [app/devices/\[id\]/page.tsx:30](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/app/devices/[id]/page.tsx#L30)

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

 - useParams and useSearchParams — to retrieve URL parameters.
 - useRouter — for navigation handling.
 - ConnectionDetails — for displaying connection info.
 - ThemeToggle — for dark/light mode toggle.
 - FiHome, FiMonitor, FiLink, FiBarChart2 — icons used in the sidebar.
