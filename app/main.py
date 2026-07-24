from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app.ai import AIAnalyzer
from app.config import get_settings
from app.exporters import businesses_to_csv
from app.models import (
    AnalysisRequest,
    AnalysisResponse,
    ExportRequest,
    ProviderStatus,
    SearchRequest,
    SearchResponse,
)
from app.providers import GooglePlacesProvider, OpenStreetMapProvider, SampleProvider
from app.providers.base import ProviderError
from app.services import SearchService

settings = get_settings()
providers = {
    "sample": SampleProvider(),
    "openstreetmap": OpenStreetMapProvider(settings),
    "google_places": GooglePlacesProvider(settings),
}
search_service = SearchService(providers)
ai_analyzer = AIAnalyzer(settings)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Discover and analyze local-business data through offline samples, OpenStreetMap, "
        "and the optional official Google Places API."
    ),
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def dashboard() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "version": "1.0.0"}


@app.get("/api/providers", response_model=list[ProviderStatus])
async def provider_statuses() -> list[ProviderStatus]:
    return [
        ProviderStatus(
            id="sample",
            label="Sample data",
            enabled=True,
            requires_key=False,
            note="Offline fictional records for demonstration.",
        ),
        ProviderStatus(
            id="openstreetmap",
            label="OpenStreetMap",
            enabled=True,
            requires_key=False,
            note="Uses public Nominatim and Overpass services; modest use only.",
        ),
        ProviderStatus(
            id="google_places",
            label="Google Places API (official)",
            enabled=bool(settings.google_places_api_key),
            requires_key=True,
            note="Add GOOGLE_PLACES_API_KEY to .env to enable.",
        ),
    ]


@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    try:
        return await search_service.search(request)
    except ProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {exc}") from exc


@app.post("/api/export/csv")
async def export_csv(request: ExportRequest) -> Response:
    csv_text = businesses_to_csv(request.businesses)
    headers = {"Content-Disposition": 'attachment; filename="geobusiness-results.csv"'}
    return Response(csv_text, media_type="text/csv; charset=utf-8", headers=headers)


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    try:
        return await ai_analyzer.analyze(request)
    except ProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI request failed: {exc}") from exc
