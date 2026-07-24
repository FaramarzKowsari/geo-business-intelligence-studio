# Protecting OpenStreetMap community services

The public Nominatim server is community-funded and intended for modest, user-triggered use. This project therefore treats upstream protection as part of its architecture rather than as an operational afterthought.

## Implemented safeguards

### Nominatim

- A stable, contactable application `User-Agent` is sent.
- Requests are serialized through a global process gate.
- Starts are spaced by at least `NOMINATIM_MIN_INTERVAL_SECONDS` (default `1.1`).
- City geocodes are cached for seven days by default.
- Expired geocodes can be used temporarily if the upstream service is unavailable.
- Concurrent identical city lookups share one upstream request.
- Only explicit form submissions trigger searches; there is no autocomplete.

### Complete searches

- Identical searches are cached for fifteen minutes by default.
- Concurrent identical searches are coalesced.
- A stale cached search can be returned during a brief provider outage.
- Public clients are limited by a process-local sliding window.
- Production deployments cap radius and record count.

### Service switching

The following values are environment variables and can be changed without a software release:

- `NOMINATIM_BASE_URL`
- `OVERPASS_BASE_URL`
- `OSM_TILE_URL`

For moderate-to-heavy or commercial traffic, configure a third-party provider or self-host Nominatim/Overpass instead of relying on the public endpoints.

## Operational boundary

The built-in limiter and cache are process-local. The Render Blueprint intentionally runs one Uvicorn worker. If the service is scaled to multiple instances, use a shared cache and distributed rate limiter, such as Render Key Value or Redis, before enabling public OpenStreetMap access across those instances.
