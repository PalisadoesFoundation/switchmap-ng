[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/Sidebar

# app/components/Sidebar

## Functions

### Sidebar()

> **Sidebar**(): `Element`

Defined in: [app/components/Sidebar.tsx:28](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/components/Sidebar.tsx#L28)

Sidebar component provides navigation links and a theme toggle button.
It supports both large screens (desktop) and small screens (mobile).

#### Returns

`Element`

The rendered sidebar component.

#### Remarks

This component is designed for client-side use only because it relies on
the `useState` and `useEffect` hooks for managing state and handling events.
It also includes responsive design features to adapt to different screen sizes.
The sidebar contains links to the dashboard, history, and settings pages,

#### See

 - [ThemeToggle](../theme-toggle.md#themetoggle) for the theme switching functionality.
 - Link for navigation links.
 - useState for managing the open/close state of the sidebar.
 - useEffect for handling side effects like closing the sidebar on outside clicks.
 - FiLayout, FiClock, FiSettings, RxHamburgerMenu for the icons used in the sidebar.
