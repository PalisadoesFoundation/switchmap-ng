[**frontend**](../../README.md)

***

[frontend](../../modules.md) / app/components/Sidebar

# app/components/Sidebar

## Functions

### Sidebar()

> **Sidebar**(): `Element`

Defined in: [app/components/Sidebar.tsx:27](https://github.com/Abhi-MS/switchmap-ng/blob/a1bd92914ced2250744e395a896ab3e110b2eb61/frontend/src/app/components/Sidebar.tsx#L27)

Sidebar component provides navigation links and a theme toggle button.
It supports both large screens (desktop) and small screens (mobile).

#### Returns

`Element`

The rendered sidebar component.

#### Remarks

This component is designed for client-side use only because it relies on
the `useState` and `useEffect` hooks for managing state and handling events.
It also includes responsive design features to adapt to different screen sizes.

#### See

 - ThemeToggle for the theme switching functionality.
 - Link for navigation links.
 - useState for managing the open/close state of the sidebar.
 - useEffect for handling click events outside the sidebar to close it.
 - FiLayout, FiClock, FiSettings for the icons used in the sidebar.

## References

### default

Renames and re-exports [Sidebar](#sidebar)
