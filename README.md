# GeoBusiness Intelligence Studio

[![CI](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)

A privacy-aware, portfolio-ready platform for discovering, normalizing, deduplicating, mapping, and exporting local-business data.

It works **without any paid API key** in Sample mode and can query OpenStreetMap through Nominatim + Overpass. Google Places and AI enrichment are optional **Bring Your Own Key** integrations.

> This repository does not scrape the Google Maps website, bypass CAPTCHAs, rotate identities, or evade access controls. The optional Google integration uses the official Places API (New).

## Features

- FastAPI backend with OpenAPI documentation
- Responsive browser dashboard
- Offline sample-data mode
- OpenStreetMap discovery with Nominatim and Overpass
- Optional official Google Places Text Search adapter
- Duplicate removal and basic data-quality scoring
- CSV and JSON export
- Optional AI analysis through Ollama or an OpenAI-compatible endpoint
- Docker and Docker Compose
- Automated tests and GitHub Actions CI
- Responsible-use, security, architecture, and Persian GitHub Desktop guides

## Quick start — no API key

### Windows

```powershell
copy .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
uvicorn app.main:app --reload
```

### macOS / Linux

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Open:

- Dashboard: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

Use provider **Sample data** to test everything offline.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

Then open `http://localhost:8000`.

## Optional providers

### OpenStreetMap

No API key is required. The public Nominatim and Overpass services are shared infrastructure. Use a truthful application User-Agent, keep requests modest, cache results in production, and operate your own instances for sustained traffic.

Set a contact address in `.env`:

```env
APP_CONTACT_EMAIL=you@example.com
```

### Google Places API (New)

1. Enable Places API (New) in Google Cloud.
2. Create and restrict an API key.
3. Put it in your local `.env`, never in Git:

```env
GOOGLE_PLACES_API_KEY=your_key_here
```

The app calls the official `POST https://places.googleapis.com/v1/places:searchText` endpoint and uses a field mask.

### Optional AI

AI is disabled by default.

#### Ollama — local, no paid key

```env
AI_PROVIDER=ollama
AI_MODEL=qwen3:4b
AI_BASE_URL=http://host.docker.internal:11434/v1
```

#### OpenAI-compatible provider

```env
AI_PROVIDER=openai_compatible
AI_MODEL=your-model
AI_BASE_URL=https://your-provider.example/v1
AI_API_KEY=your_key_here
```

The core search and export features do not depend on AI.

## API example

```bash
curl -X POST http://127.0.0.1:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "sample",
    "query": "coffee",
    "city": "Amsterdam",
    "radius_m": 5000,
    "limit": 20
  }'
```

## Project structure

```text
app/
├── main.py                  FastAPI routes and static dashboard
├── config.py                Environment configuration
├── models.py                Pydantic request/response models
├── services.py              Search orchestration, normalization, dedupe
├── exporters.py             CSV export
├── ai.py                    Optional Ollama/OpenAI-compatible analysis
├── providers/
│   ├── sample.py            Offline provider
│   ├── overpass.py          OpenStreetMap provider
│   └── google_places.py     Official Google Places provider
└── static/                  Browser UI
```

## Tests

```bash
pytest
```

## Publishing with GitHub Desktop

Read [`docs/GITHUB_DESKTOP_GUIDE_FA.md`](docs/GITHUB_DESKTOP_GUIDE_FA.md).

## Responsible use

Read [`docs/RESPONSIBLE_USE.md`](docs/RESPONSIBLE_USE.md). Verify records before acting on them, respect provider terms and rate limits, minimize personal-data collection, and never use the project for harassment, spam, surveillance, or access-control evasion.

## Credits

OpenStreetMap data is © OpenStreetMap contributors and available under ODbL. The browser map uses OpenStreetMap tiles with visible attribution. Google Places data, when enabled, is obtained through the user's own official API credentials and remains subject to Google Maps Platform terms.

## License

MIT © 2026 Faramarz Kowsari
