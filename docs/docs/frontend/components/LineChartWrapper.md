[**frontend**](../README.md)

***

[frontend](../modules.md) / components/LineChartWrapper

# components/LineChartWrapper

## Functions

### LineChartWrapper()

> **LineChartWrapper**(`__namedParameters`): `Element`

Defined in: [components/LineChartWrapper.tsx:66](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/components/LineChartWrapper.tsx#L66)

LineChartWrapper is a reusable component for rendering line charts with Recharts.
It abstracts the common configuration for line charts, including axes, tooltips, and lines.
This allows for consistent styling and behavior across different charts in the application.

#### Parameters

##### \_\_namedParameters

`LineChartWrapperProps`

#### Returns

`Element`

The rendered line chart component.

#### Remarks

This component is designed to be flexible and reusable, allowing developers to pass in data,
x-axis keys, line configurations, and y-axis settings.
It supports custom tooltips and titles, making it suitable for various charting needs.

#### See

 - [ResponsiveContainer](#) for responsive layout.
 - [LineChart](#), [XAxis](#), [YAxis](#), [Tooltip](#), [Line](#) from Recharts for chart rendering.
*

## References

### default

Renames and re-exports [LineChartWrapper](#linechartwrapper)
