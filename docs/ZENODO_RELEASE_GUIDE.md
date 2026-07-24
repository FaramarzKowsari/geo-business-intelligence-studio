# Zenodo DOI Release Guide

This repository is prepared for Zenodo with:

- `CITATION.cff` for GitHub's citation panel;
- `.zenodo.json` for Zenodo-specific release metadata;
- `codemeta.json` for interoperable software metadata.

## Recommended first archived release

- Tag: `v1.0.0`
- Release title: `GeoBusiness Intelligence Studio v1.0.0`
- Resource type: Software
- Access: Open
- License: MIT
- Creator: Faramarz Kowsari
- ORCID: 0000-0003-1692-0453

## Release description

> GeoBusiness Intelligence Studio is a privacy-aware FastAPI platform for discovering, normalizing, deduplicating, mapping, analyzing, and exporting local-business records. It supports fictional offline samples, OpenStreetMap through Nominatim and Overpass, the optional official Google Places API, deterministic analysis without AI, and optional Ollama or OpenAI-compatible BYOK analysis.

## Steps

1. Sign in to Zenodo using the GitHub or ORCID account connected to this repository.
2. Open the Zenodo GitHub integration page.
3. Click **Sync now** and enable `FaramarzKowsari/geo-business-intelligence-studio`.
4. In GitHub, create the `v1.0.0` release from the current `main` branch.
5. Wait for Zenodo to archive the release and mint the version-specific DOI.
6. Copy the DOI into `README.md`, `CITATION.cff`, `codemeta.json`, `docs/index.html`, and the guidebook citation section.
7. Commit the DOI update as a documentation-only change.

## Citation template after DOI minting

> Kowsari, F. (2026). *GeoBusiness Intelligence Studio: An Open-Data Platform for Business Discovery, Mapping, Data Quality, and Optional BYOK AI* (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/REPLACE_WITH_DOI

Do not invent or pre-fill a DOI. Use only the identifier shown on the published Zenodo record.
