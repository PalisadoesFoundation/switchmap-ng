[**frontend**](../README.md)

***

[frontend](../modules.md) / app/theme-toggle

# app/theme-toggle

## Functions

### ThemeToggle()

> **ThemeToggle**(): `null` \| `Element`

Defined in: [app/theme-toggle.tsx:23](https://github.com/Abhi-MS/switchmap-ng/blob/541e84ce7b8b339a438f8adc6def2b02b4cae6cf/frontend/src/app/theme-toggle.tsx#L23)

ThemeToggle component allows users to switch between light and dark themes.
It uses the Next.js `useTheme` hook to manage the theme state.
The component renders a button that toggles the theme when clicked.

#### Returns

`null` \| `Element`

The rendered component.

#### Remarks

This component is designed for client-side use only because it relies on
the `useTheme` hook, which is not available during server-side rendering.
It also ensures the component is mounted before rendering to avoid SSR mismatches.
The icons used for the toggle come from the `react-icons` library.

#### See

 - useTheme for managing themes in Next.js.
 - FiSun and FiMoon for the icons used in the toggle button.
