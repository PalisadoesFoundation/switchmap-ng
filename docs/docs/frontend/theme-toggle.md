[**frontend**](README.md)

***

[frontend](modules.md) / theme-toggle

# theme-toggle

## Functions

### ThemeToggle()

> **ThemeToggle**(): `null` \| `Element`

Defined in: [theme-toggle.tsx:20](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/theme-toggle.tsx#L20)

A toggle button to switch between light and dark themes.

#### Returns

`null` \| `Element`

A button element that toggles the theme on click.

#### Remarks

This component uses the `next-themes` library to manage theme state and
persists the user's preference in local storage. It displays a sun icon
when the dark theme is active and a moon icon when the light theme is active.

#### See

 - [useTheme](#) from `next-themes` for theme management.
 - [FiSun](#) and [FiMoon](#) from `react-icons/fi` for the icons used.
