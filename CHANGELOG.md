# Changelog

## 1.2.0 — 2026-07-24

- Added a Render Blueprint for browser-only public deployment.
- Added a Windows desktop launcher with a visible start/stop controller.
- Added a Windows GitHub Actions workflow that builds, smoke-tests, hashes, and uploads a self-contained EXE.
- Added Nominatim and Overpass request spacing, geocoding cache, complete-search cache, stale fallback, and simultaneous-request coalescing.
- Added per-client public OpenStreetMap limits and production caps on radius and result count.
- Made Nominatim, Overpass, and map-tile endpoints configurable without a software update.
- Added deployment, Windows distribution, and OpenStreetMap service-protection documentation.
- Updated project metadata and public pages to version 1.2.0.

## 1.0.0 — 2026-07-23

- Added FastAPI application and responsive browser dashboard.
- Added offline sample-data provider.
- Added OpenStreetMap Nominatim and Overpass provider.
- Added optional official Google Places API (New) adapter.
- Added duplicate detection and data-quality scoring.
- Added CSV and JSON export.
- Added deterministic analysis and optional Ollama/OpenAI-compatible AI.
- Added Docker, GitHub Actions CI, tests, security guidance, and Persian GitHub Desktop instructions.
