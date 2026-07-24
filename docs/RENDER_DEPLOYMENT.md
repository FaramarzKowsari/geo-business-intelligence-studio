# Render deployment

GeoBusiness Intelligence Studio includes a root-level `render.yaml` Blueprint. It deploys one FastAPI web service, binds Uvicorn to Render's `$PORT`, uses a single worker so the process-wide OpenStreetMap request gate remains authoritative, and checks `/api/health` during deploys.

## One-click path

1. Open `https://render.com/deploy?repo=https://github.com/FaramarzKowsari/geo-business-intelligence-studio`.
2. Sign in to Render and authorize the GitHub repository.
3. Review the Blueprint and create the web service.
4. After deployment, open the assigned `onrender.com` URL.
5. If Render assigns a hostname different from the expected project name, set `PUBLIC_BASE_URL` to the final HTTPS URL.

The free service tier can sleep after inactivity. Its first request after sleeping can take longer while the service starts.

## Optional keys

The public deployment requires no paid key. Add these only in Render's Environment page, never in Git:

- `GOOGLE_PLACES_API_KEY`
- `AI_PROVIDER`
- `AI_MODEL`
- `AI_BASE_URL`
- `AI_API_KEY`

## OpenStreetMap safety defaults

The Blueprint runs a single worker and enables:

- a minimum 1.1-second interval between Nominatim requests;
- a minimum interval between Overpass requests;
- a seven-day city-geocoding cache;
- a fifteen-minute full-search cache;
- stale-cache fallback during brief upstream failures;
- coalescing of simultaneous identical searches;
- a per-client OpenStreetMap search limit;
- public radius and result-count caps;
- configurable Nominatim, Overpass, and tile endpoints.

For sustained traffic, replace public OSMF endpoints with a dedicated provider or self-hosted infrastructure through environment variables.
