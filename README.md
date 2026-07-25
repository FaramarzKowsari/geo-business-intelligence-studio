<div align="center">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4" alt="Faramarz Kowsari" width="116" />

# GeoBusiness Intelligence Studio

### An Open-Data Platform for Business Discovery, Mapping, Data Quality, and Optional BYOK AI

[![CI](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/ci.yml)
[![Pages](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/deploy-pages.yml)
[![Windows build](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/build-windows.yml/badge.svg)](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions/workflows/build-windows.yml)
[![Live Application](https://img.shields.io/badge/Live%20Application-Open%20in%20Browser-46e3b7.svg)](https://geo-business-intelligence-studio.onrender.com)
[![Windows EXE](https://img.shields.io/badge/Windows-Download%20EXE-0078D4.svg?logo=windows)](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21539094.svg)](https://doi.org/10.5281/zenodo.21539094)
[![License: MIT](https://img.shields.io/badge/License-MIT-45d9e8.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776ab.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-OpenAPI-009688.svg)](https://fastapi.tiangolo.com/)

**Project site:** `https://faramarzkowsari.github.io/geo-business-intelligence-studio/`  
**Live application:** `https://geo-business-intelligence-studio.onrender.com`  
**Windows edition:** [Download the latest verified EXE](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe)  
**Visual guidebook:** `https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/`  
**Zenodo DOI:** [10.5281/zenodo.21539094](https://doi.org/10.5281/zenodo.21539094)  
**Source code:** `https://github.com/FaramarzKowsari/geo-business-intelligence-studio`

</div>

<p align="center">
  <a href="https://faramarzkowsari.github.io/geo-business-intelligence-studio/">
    <img src="docs/assets/geobusiness-hero.svg" alt="GeoBusiness Intelligence Studio architecture and interface overview" width="100%" />
  </a>
</p>

GeoBusiness Intelligence Studio is a privacy-aware FastAPI platform for discovering, normalizing, deduplicating, mapping, analyzing, and exporting local-business records. The core application works without a paid AI key. It supports fictional offline samples and OpenStreetMap through Nominatim and Overpass; Google Places and model-based analysis remain optional Bring Your Own Key integrations.

The repository separates provider evidence, deterministic processing, and optional AI interpretation. It does not scrape the Google Maps website, bypass CAPTCHAs, rotate identities, or evade access controls.

## Use the application

### Browser - no installation

[**Launch GeoBusiness Intelligence Studio**](https://geo-business-intelligence-studio.onrender.com)

The hosted Render edition runs in the browser. No Python, PowerShell, package installation, or AI key is required for the core workflow. Free Render instances can take several seconds to wake after inactivity.

### Windows - no Python or PowerShell

[**Download GeoBusiness Intelligence Studio for Windows**](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe)

[Download the SHA-256 verification file](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe.sha256)

The official one-file Windows application is built and smoke-tested on a GitHub-hosted Windows runner. Double-click `GeoBusiness-Intelligence-Studio.exe`; it starts a localhost-only FastAPI server and opens the dashboard in the default browser. Windows SmartScreen may show an unknown-publisher warning because the executable is not code-signed.

### Source and Docker

Developers can inspect, test, extend, and privately deploy the full source using Python or Docker. See the quick-start section below.

## Visual guidebook

**Inside GeoBusiness Intelligence Studio - A Visual Guide to Open Data, Geospatial Discovery, and Local Business Intelligence**

- [Read the responsive guidebook](https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/)
- [Open or download the A4 PDF](https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/inside-geobusiness-intelligence-studio.pdf)
- [Guidebook documentation](docs/GUIDEBOOK.md)

The ten-section guidebook covers the project purpose, providers, end-to-end workflow, interface, architecture, normalization, data quality, duplicate detection, responsible use, deployment, citation, and author information.

## Canonical project links

- [Launch the hosted application](https://geo-business-intelligence-studio.onrender.com)
- [Download the latest Windows EXE](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe)
- [Download the Windows SHA-256 file](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases/latest/download/GeoBusiness-Intelligence-Studio.exe.sha256)
- [Public project site](https://faramarzkowsari.github.io/geo-business-intelligence-studio/)
- [Visual guidebook](https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/)
- [Guidebook PDF](https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/inside-geobusiness-intelligence-studio.pdf)
- [GitHub Releases](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/releases)
- [Zenodo software record](https://doi.org/10.5281/zenodo.21539094)
- [Source repository](https://github.com/FaramarzKowsari/geo-business-intelligence-studio)
- [Continuous integration results](https://github.com/FaramarzKowsari/geo-business-intelligence-studio/actions)

## What it can do

- run immediately with fictional offline sample records;
- discover places through OpenStreetMap using Nominatim and Overpass;
- optionally query the official Google Places API;
- normalize provider-specific responses into a shared business model;
- preserve source provenance;
- calculate an interpretable data-completeness score;
- remove probable duplicates using phone equality and name/address similarity;
- visualize coordinates on a Leaflet map;
- export results as CSV or JSON;
- generate a deterministic dataset briefing without AI;
- optionally use Ollama or an OpenAI-compatible BYOK endpoint;
- expose interactive OpenAPI documentation through FastAPI;
- deploy through a Render Blueprint;
- build a self-contained Windows EXE through GitHub Actions;
- protect community OpenStreetMap services with caching, coalescing, request spacing, and client limits.

## Verified live OpenStreetMap search

<p align="center">
  <img src="docs/assets/geobusiness-live-search.svg" alt="Live OpenStreetMap coffee-business search in Amsterdam returning 29 normalized records" width="100%" />
</p>

The demonstrated search returned 29 records after removing one probable duplicate. Phone coverage was 31%, website coverage was 55%, and the average completeness score was 69/100. Provider coverage varies by region, and contact data must be verified before operational use.

## Evidence and responsibility labels

| Layer | Meaning |
|---|---|
| **Provider record** | Data returned by Sample, OpenStreetMap, or the optional official Google Places adapter. |
| **Normalized record** | A provider response converted into the shared internal business schema. |
| **Quality score** | A completeness indicator, not proof that the business data is correct or current. |
| **Probable duplicate** | An inferred duplicate based on stronger and softer matching evidence. |
| **Deterministic briefing** | A built-in statistical summary generated without a model. |
| **AI analysis** | Optional model interpretation; it is not source evidence. |

## OpenStreetMap community-service protection

The public Nominatim endpoint is not treated as an unlimited backend. Version 1.2 includes:

- a stable and contactable application User-Agent;
- at least 1.1 seconds between Nominatim request starts;
- process-wide serialized upstream calls;
- seven-day city-geocoding cache and fifteen-minute full-search cache;
- stale-cache fallback during short upstream failures;
- coalescing of simultaneous identical requests;
- per-client public search limits;
- production caps on radius and returned records;
- environment-configurable Nominatim, Overpass, and tile endpoints.

The Render Blueprint runs one worker so the process-level gate remains authoritative. Multi-instance deployments require a shared cache and distributed limiter or dedicated OSM infrastructure. See [OSM service protection](docs/OSM_SERVICE_PROTECTION.md).

## Quick start - developers

### Windows PowerShell

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### macOS / Linux

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m uvicorn app.main:app --reload
```

Open:

- Dashboard: `http://127.0.0.1:8000`
- API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

Use provider **Sample data - offline** to test without network access.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

Open `http://localhost:8000`.

## Optional integrations

### Google Places API

```env
GOOGLE_PLACES_API_KEY=your_restricted_key
```

### Local Ollama

```env
AI_PROVIDER=ollama
AI_MODEL=qwen3:4b
AI_BASE_URL=http://host.docker.internal:11434/v1
```

### OpenAI-compatible provider

```env
AI_PROVIDER=openai_compatible
AI_MODEL=your-model
AI_BASE_URL=https://your-provider.example/v1
AI_API_KEY=your_key
```

The discovery, mapping, quality, deduplication, and export path does not depend on AI.

## Technical and scholarly documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Responsible use](docs/RESPONSIBLE_USE.md)
- [Security policy](SECURITY.md)
- [Windows edition](docs/WINDOWS_EDITION.md)
- [Render deployment](docs/RENDER_DEPLOYMENT.md)
- [OSM service protection](docs/OSM_SERVICE_PROTECTION.md)
- [Guidebook](docs/GUIDEBOOK.md)
- [Zenodo DOI and releases](docs/ZENODO_RELEASE_GUIDE.md)
- [Google Search Console](docs/SEARCH_CONSOLE_GUIDE.md)
- [Post-release checklist](docs/POST_RELEASE_CHECKLIST.md)
- [Machine-readable summary](docs/llms.txt)

## Tests and continuous integration

```bash
python -m ruff check .
python -m pytest
```

The CI matrix checks supported Python versions. Separate workflows deploy GitHub Pages and build, launch, health-check, checksum, and publish the Windows executable.

## Author

**Faramarz Kowsari** is an author, Software Engineer and AI researcher based in Istanbul. Focusing on the intersection of technology, education, and personal growth, he has published over 80 digital titles on international platforms. His areas of expertise span Artificial Intelligence, prompt engineering, modern trading strategies (Smart Money Concepts and algorithmic trading), classical literature, and mindfulness. He also develops web-based educational tools and specialized instructional video content.

### Official profiles

- ORCID: https://orcid.org/0000-0003-1692-0453
- Google Scholar: https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en
- GitHub: https://github.com/FaramarzKowsari
- LinkedIn: https://www.linkedin.com/in/faramarzkowsari
- Google Books: https://play.google.com/store/search?q=Faramarz_Kowsari&c=books
- Official website: https://FaramarzKowsari.github.io
- Zenodo DOI: https://doi.org/10.5281/zenodo.21539094

## Citation

> Kowsari, F. (2026). *GeoBusiness Intelligence Studio: An Open-Data Platform for Business Discovery, Mapping, Data Quality, and Optional BYOK AI* (Version 1.2.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21539094

Machine-readable metadata is available in [`CITATION.cff`](CITATION.cff), [`.zenodo.json`](.zenodo.json), and [`codemeta.json`](codemeta.json).

## License

MIT © 2026 Faramarz Kowsari.
