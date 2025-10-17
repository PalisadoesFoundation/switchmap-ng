[**frontend**](../README.md)

***

[frontend](../modules.md) / config/page

# config/page

## Functions

### \_\_resetConfigCache()

> **\_\_resetConfigCache**(): `void`

Defined in: [config/page.tsx:86](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/config/page.tsx#L86)

#### Returns

`void`

***

### default()

> **default**(): `Element`

Defined in: [config/page.tsx:99](https://github.com/PalisadoesFoundation/switchmap-ng/blob/develop/frontend/src/app/config/page.tsx#L99)

ConfigPage component for managing Switchmap configuration.

Optimizations:
- In-memory caching of config data with TTL
- Memoized computed values
- Request cancellation with AbortController using useRef
- Optimistic UI updates

#### Returns

`Element`
