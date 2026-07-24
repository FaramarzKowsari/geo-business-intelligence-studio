# API Guide

Interactive documentation is available at `/docs` while the application runs.

## `GET /api/health`

Returns application status and version.

## `GET /api/providers`

Returns provider availability and whether a key is required.

## `POST /api/search`

```json
{
  "provider": "sample",
  "query": "coffee",
  "city": "Amsterdam",
  "radius_m": 5000,
  "limit": 30,
  "language": "en",
  "deduplicate": true
}
```

Provider values: `sample`, `openstreetmap`, `google_places`.

## `POST /api/export/csv`

Accepts a `businesses` array matching the search response and returns a CSV attachment.

## `POST /api/analyze`

```json
{
  "businesses": [],
  "instruction": "Summarize market patterns and data gaps."
}
```

With `AI_PROVIDER=none`, this endpoint produces a deterministic briefing. With Ollama or another OpenAI-compatible endpoint configured, it uses the selected model.
