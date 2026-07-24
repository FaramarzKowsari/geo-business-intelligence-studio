from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
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
from app.traffic import SlidingWindowLimiter

settings = get_settings()
providers = {
    "sample": SampleProvider(),
    "openstreetmap": OpenStreetMapProvider(settings),
    "google_places": GooglePlacesProvider(settings),
}
search_service = SearchService(providers, settings)
ai_analyzer = AIAnalyzer(settings)
client_limiter = SlidingWindowLimiter()

app = FastAPI(
    title=settings.app_name,
    version="1.2.0",
    description=(
        "Discover and analyze local-business data through offline samples, OpenStreetMap, "
        "and the optional official Google Places API. Public OSM access is protected with "
        "caching, request coalescing, client limits, and globally spaced upstream calls."
    ),
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def dashboard() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/api/health")
async def health() -> dict[str, str | int]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": "1.2.0",
        "environment": settings.app_env,
        "search_cache_entries": await search_service.cache_size(),
    }


@app.get("/api/runtime-config")
async def runtime_config() -> dict[str, str | bool]:
    return {
        "tile_url": settings.osm_tile_url,
        "environment": settings.app_env,
        "public_osm_enabled": settings.public_osm_enabled,
    }


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
            enabled=settings.public_osm_enabled,
            requires_key=False,
            note=(
                "Protected by geocoding/search caches, request coalescing, a global Nominatim "
                "interval, an Overpass interval, and a per-client public rate limit."
            ),
        ),
        ProviderStatus(
            id="google_places",
            label="Google Places API (official)",
            enabled=bool(settings.google_places_api_key),
            requires_key=True,
            note="Add GOOGLE_PLACES_API_KEY as a secret environment variable to enable.",
        ),
    ]


def _client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    return forwarded or (request.client.host if request.client else "unknown")


@app.post("/api/search", response_model=SearchResponse)
async def search(
    payload: SearchRequest,
    request: Request,
    response: Response,
) -> SearchResponse:
    if payload.provider.value == "openstreetmap":
        if not settings.public_osm_enabled:
            raise HTTPException(status_code=503, detail="Public OpenStreetMap search is disabled.")
        if settings.is_public_deployment:
            if payload.limit > settings.public_osm_max_records:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        "Public OpenStreetMap searches are limited to "
                        f"{settings.public_osm_max_records} records."
                    ),
                )
            if payload.radius_m > settings.public_osm_max_radius_m:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        "Public OpenStreetMap searches are limited to a "
                        f"{settings.public_osm_max_radius_m} metre radius."
                    ),
                )
        allowed, retry_after = await client_limiter.allow(
            f"osm::{_client_key(request)}",
            max_requests=settings.public_osm_requests_per_minute,
            window_seconds=60,
        )
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Too many OpenStreetMap searches. Please wait before trying again.",
                headers={"Retry-After": str(retry_after)},
            )
        response.headers["X-RateLimit-Limit"] = str(settings.public_osm_requests_per_minute)
        response.headers["X-OpenStreetMap-Safeguards"] = "cache,coalescing,global-spacing"

    try:
        result = await search_service.search(payload)
        response.headers["X-GeoBusiness-Cache"] = "HIT" if result.meta.cache_hit else "MISS"
        return result
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
