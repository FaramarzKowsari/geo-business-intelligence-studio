from __future__ import annotations

import asyncio
import re
from collections.abc import Awaitable, Callable

import httpx

from app.config import Settings
from app.models import Business, SearchRequest
from app.providers.base import BusinessProvider, ProviderError
from app.traffic import AsyncRateGate, AsyncRequestCoalescer, AsyncTTLCache

CATEGORY_RULES: list[tuple[tuple[str, ...], tuple[str, str]]] = [
    (("coffee", "cafe", "café"), ("amenity", "cafe")),
    (("restaurant", "food"), ("amenity", "restaurant")),
    (("bar", "pub"), ("amenity", "pub")),
    (("gym", "fitness"), ("leisure", "fitness_centre")),
    (("dentist", "dental"), ("amenity", "dentist")),
    (("pharmacy", "chemist"), ("amenity", "pharmacy")),
    (("hospital", "clinic"), ("amenity", "clinic")),
    (("hotel", "hostel"), ("tourism", "hotel")),
    (("supermarket", "grocery"), ("shop", "supermarket")),
    (("bakery", "bread"), ("shop", "bakery")),
    (("school", "academy"), ("amenity", "school")),
    (("bank",), ("amenity", "bank")),
    (("hair", "barber", "hairdresser"), ("shop", "hairdresser")),
    (("software", "technology", "it company"), ("office", "it")),
]


class OpenStreetMapProvider(BusinessProvider):
    id = "openstreetmap"
    label = "OpenStreetMap"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._geocode_cache: AsyncTTLCache[tuple[float, float, str]] = AsyncTTLCache(512)
        self._geocode_coalescer: AsyncRequestCoalescer[tuple[float, float, str]] = (
            AsyncRequestCoalescer()
        )
        self._nominatim_gate = AsyncRateGate(settings.nominatim_min_interval_seconds)
        self._overpass_gate = AsyncRateGate(settings.overpass_min_interval_seconds)

    def _headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": self.settings.user_agent,
            "Accept": "application/json",
        }
        if self.settings.public_base_url:
            headers["Referer"] = self.settings.public_base_url
        return headers

    async def _request_with_one_retry(
        self,
        *,
        gate: AsyncRateGate,
        operation: Callable[[], Awaitable[httpx.Response]],
        service_name: str,
    ) -> httpx.Response:
        for attempt in range(2):
            await gate.wait()
            response = await operation()
            if response.status_code not in {429, 502, 503, 504} or attempt == 1:
                return response
            retry_after = response.headers.get("Retry-After", "")
            try:
                delay = min(max(float(retry_after), 1.1), 10.0)
            except ValueError:
                delay = 2.0
            await asyncio.sleep(delay)
        raise ProviderError(f"{service_name} request could not be completed.")

    async def _fetch_geocode(self, city: str, language: str) -> tuple[float, float, str]:
        params = {
            "q": city,
            "format": "jsonv2",
            "limit": 1,
            "addressdetails": 1,
            "accept-language": language,
        }
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await self._request_with_one_retry(
                gate=self._nominatim_gate,
                service_name="Nominatim",
                operation=lambda: client.get(
                    f"{self.settings.nominatim_base_url.rstrip('/')}/search",
                    params=params,
                    headers=self._headers(),
                ),
            )
        if response.status_code == 403:
            raise ProviderError(
                "Nominatim rejected the request. Verify APP_CONTACT_EMAIL and the configured "
                "NOMINATIM_BASE_URL, or switch to a dedicated geocoding provider."
            )
        if response.status_code == 429:
            raise ProviderError("Nominatim rate limit reached. Wait before retrying.")
        response.raise_for_status()
        rows = response.json()
        if not rows:
            raise ProviderError(f"Could not geocode city: {city}")
        row = rows[0]
        return float(row["lat"]), float(row["lon"]), row.get("display_name", city)

    async def _geocode(self, city: str, language: str) -> tuple[float, float, str]:
        key = f"{language.casefold()}::{city.casefold().strip()}"
        cached = await self._geocode_cache.get(key)
        if cached.value is not None:
            return cached.value

        async def fetch_and_cache() -> tuple[float, float, str]:
            try:
                value = await self._fetch_geocode(city, language)
            except (httpx.HTTPError, ProviderError):
                stale = await self._geocode_cache.get(key, allow_stale=True)
                if stale.value is not None:
                    return stale.value
                raise
            await self._geocode_cache.set(
                key,
                value,
                ttl_seconds=self.settings.geocode_cache_ttl_seconds,
                stale_ttl_seconds=self.settings.geocode_stale_ttl_seconds,
            )
            return value

        return await self._geocode_coalescer.run(key, fetch_and_cache)

    @staticmethod
    def _rule_for(query: str) -> tuple[str, str] | None:
        lowered = query.casefold()
        for aliases, rule in CATEGORY_RULES:
            if any(alias in lowered for alias in aliases):
                return rule
        return None

    @staticmethod
    def _safe_regex(value: str) -> str:
        value = re.sub(r"[^\w\s\-]", " ", value, flags=re.UNICODE)
        value = " ".join(value.split())
        return re.escape(value[:60])

    def _build_query(self, request: SearchRequest, lat: float, lon: float) -> str:
        rule = self._rule_for(request.query)
        around = f"around:{request.radius_m},{lat},{lon}"
        if rule:
            key, value = rule
            selector = f'["{key}"="{value}"]'
        else:
            regex = self._safe_regex(request.query)
            selector = f'["name"~"{regex}",i]'
        return (
            "[out:json][timeout:25];"
            "("
            f"node({around}){selector};"
            f"way({around}){selector};"
            f"relation({around}){selector};"
            ");"
            "out center tags;"
        )

    async def search(self, request: SearchRequest) -> list[Business]:
        lat, lon, geocoded_name = await self._geocode(request.city, request.language)
        query = self._build_query(request, lat, lon)
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds + 10) as client:
            response = await self._request_with_one_retry(
                gate=self._overpass_gate,
                service_name="Overpass",
                operation=lambda: client.post(
                    self.settings.overpass_base_url,
                    data={"data": query},
                    headers=self._headers(),
                ),
            )
        if response.status_code == 429:
            raise ProviderError("Overpass is busy or rate-limiting this request. Retry later.")
        response.raise_for_status()
        elements = response.json().get("elements", [])
        businesses: list[Business] = []
        for element in elements:
            tags = element.get("tags", {})
            name = tags.get("name")
            if not name:
                continue
            center = element.get("center", {})
            element_lat = element.get("lat", center.get("lat"))
            element_lon = element.get("lon", center.get("lon"))
            category = (
                tags.get("amenity")
                or tags.get("shop")
                or tags.get("office")
                or tags.get("tourism")
                or tags.get("leisure")
                or "business"
            ).replace("_", " ")
            street = " ".join(
                value
                for value in [tags.get("addr:housenumber", ""), tags.get("addr:street", "")]
                if value
            )
            address = ", ".join(
                value
                for value in [street, tags.get("addr:postcode", ""), tags.get("addr:city", "")]
                if value
            )
            osm_type = element.get("type", "node")
            osm_id = element.get("id")
            businesses.append(
                Business(
                    id=f"osm-{osm_type}-{osm_id}",
                    name=name,
                    category=category,
                    address=address or geocoded_name,
                    city=tags.get("addr:city", request.city),
                    country=tags.get("addr:country", ""),
                    phone=tags.get("contact:phone", tags.get("phone", "")),
                    website=tags.get("contact:website", tags.get("website", "")),
                    email=tags.get("contact:email", tags.get("email", "")),
                    latitude=element_lat,
                    longitude=element_lon,
                    source="openstreetmap",
                    source_url=f"https://www.openstreetmap.org/{osm_type}/{osm_id}",
                    raw={"osm_tags": tags},
                )
            )
            if len(businesses) >= request.limit:
                break
        return businesses
