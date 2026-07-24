# Architecture

## Design goals

1. Run immediately without paid services.
2. Keep external data providers behind adapters.
3. Make paid or sensitive credentials optional and local.
4. Avoid direct Google Maps website scraping and access-control evasion.
5. Make data provenance visible on every record.
6. Keep the first release understandable enough for portfolio review.

## Components

### Browser dashboard

A static HTML/CSS/JavaScript application served by FastAPI. It performs same-origin API calls and uses Leaflet for optional map rendering.

### FastAPI application

Routes validate requests with Pydantic, call the search service, export CSV, and invoke optional analysis.

### Provider adapters

- `SampleProvider`: fictional offline records.
- `OpenStreetMapProvider`: Nominatim geocoding followed by Overpass read-only queries.
- `GooglePlacesProvider`: official Places API (New) Text Search using the user's own key.

All providers implement the same `BusinessProvider.search()` interface.

### Search service

Normalizes returned records, calculates a data-completeness score, sorts results, and removes probable duplicates using phone equality and name/address similarity.

### AI analyzer

When disabled, a deterministic statistical briefing is generated. When enabled, the application calls an OpenAI-compatible `/chat/completions` endpoint, allowing Ollama or a commercial provider without adding provider SDK dependencies.

## Production extensions

A serious multi-user deployment should add:

- PostgreSQL/PostGIS
- Redis and a job queue
- authentication and per-user authorization
- server-side caching
- provider-specific quotas
- encrypted secret storage
- audit logs and deletion workflows
- background jobs with bounded retries
- dedicated geocoding/Overpass infrastructure
- observability and structured logging
