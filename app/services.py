from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from difflib import SequenceMatcher

import httpx

from app.config import Settings
from app.models import Business, SearchMeta, SearchRequest, SearchResponse
from app.providers.base import BusinessProvider, ProviderError
from app.traffic import AsyncRequestCoalescer, AsyncTTLCache


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.casefold()
    return re.sub(r"[^\w]+", "", value, flags=re.UNICODE)


def quality_score(business: Business) -> int:
    score = 20 if business.name else 0
    score += 15 if business.category else 0
    score += 15 if business.address else 0
    score += 15 if business.phone else 0
    score += 15 if business.website else 0
    score += 10 if business.email else 0
    score += 5 if business.latitude is not None and business.longitude is not None else 0
    score += 5 if business.rating is not None else 0
    return min(score, 100)


def is_duplicate(left: Business, right: Business) -> bool:
    left_phone = normalize_text(left.phone)
    right_phone = normalize_text(right.phone)
    if left_phone and right_phone and left_phone == right_phone:
        return True

    left_name = normalize_text(left.name)
    right_name = normalize_text(right.name)
    if not left_name or not right_name:
        return False
    name_similarity = SequenceMatcher(None, left_name, right_name).ratio()

    left_address = normalize_text(left.address)
    right_address = normalize_text(right.address)
    address_similarity = (
        SequenceMatcher(None, left_address, right_address).ratio()
        if left_address and right_address
        else 0.0
    )
    return name_similarity >= 0.94 or (name_similarity >= 0.84 and address_similarity >= 0.72)


def deduplicate_businesses(items: list[Business]) -> tuple[list[Business], int]:
    unique: list[Business] = []
    removed = 0
    for item in items:
        if any(is_duplicate(item, existing) for existing in unique):
            removed += 1
            continue
        unique.append(item)
    return unique, removed


class SearchService:
    def __init__(self, providers: dict[str, BusinessProvider], settings: Settings) -> None:
        self.providers = providers
        self.settings = settings
        self._cache: AsyncTTLCache[SearchResponse] = AsyncTTLCache(512)
        self._coalescer: AsyncRequestCoalescer[SearchResponse] = AsyncRequestCoalescer()

    @staticmethod
    def _cache_key(request: SearchRequest) -> str:
        payload = json.dumps(request.model_dump(mode="json"), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _cache_policy(self, provider: str) -> tuple[int, int]:
        if provider == "openstreetmap":
            return (
                self.settings.osm_search_cache_ttl_seconds,
                self.settings.osm_search_stale_ttl_seconds,
            )
        if provider == "google_places":
            return self.settings.google_search_cache_ttl_seconds, 0
        return 3600, 0

    async def _search_uncached(self, request: SearchRequest) -> SearchResponse:
        provider = self.providers[request.provider.value]
        businesses = await provider.search(request)
        for business in businesses:
            business.quality_score = quality_score(business)
        businesses.sort(key=lambda item: (item.quality_score, item.rating or 0), reverse=True)

        removed = 0
        if request.deduplicate:
            businesses, removed = deduplicate_businesses(businesses)

        warnings: list[str] = []
        if request.provider.value == "openstreetmap":
            warnings.extend(
                [
                    "OpenStreetMap coverage varies by region. Verify contact fields before use.",
                    "Public OSM services are protected by caching and global request spacing.",
                ]
            )
        if request.provider.value == "sample":
            warnings.append("Sample records are fictional and intended only for demonstration.")

        return SearchResponse(
            businesses=businesses[: request.limit],
            meta=SearchMeta(
                provider=request.provider.value,
                query=request.query,
                city=request.city,
                returned=min(len(businesses), request.limit),
                duplicates_removed=removed,
                warnings=warnings,
            ),
        )

    async def search(self, request: SearchRequest) -> SearchResponse:
        key = self._cache_key(request)
        cached = await self._cache.get(key)
        if cached.value is not None:
            response = cached.value.model_copy(deep=True)
            response.meta.cache_hit = True
            response.meta.cache_age_seconds = round(cached.age_seconds or 0)
            return response

        async def fetch_and_cache() -> SearchResponse:
            try:
                response = await self._search_uncached(request)
            except (ProviderError, httpx.HTTPError):
                stale = await self._cache.get(key, allow_stale=True)
                if stale.value is not None:
                    response = stale.value.model_copy(deep=True)
                    response.meta.cache_hit = True
                    response.meta.cache_stale = True
                    response.meta.cache_age_seconds = round(stale.age_seconds or 0)
                    response.meta.warnings.append(
                        "The upstream service was unavailable; a stale cached result was returned."
                    )
                    return response
                raise
            ttl, stale_ttl = self._cache_policy(request.provider.value)
            if ttl > 0:
                await self._cache.set(
                    key,
                    response.model_copy(deep=True),
                    ttl_seconds=ttl,
                    stale_ttl_seconds=stale_ttl,
                )
            return response

        return await self._coalescer.run(key, fetch_and_cache)

    async def cache_size(self) -> int:
        return await self._cache.size()
