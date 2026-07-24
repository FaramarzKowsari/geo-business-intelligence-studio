from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ProviderName(StrEnum):
    sample = "sample"
    openstreetmap = "openstreetmap"
    google_places = "google_places"


class Business(BaseModel):
    id: str
    name: str
    category: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    phone: str = ""
    website: str = ""
    email: str = ""
    latitude: float | None = None
    longitude: float | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    source: str
    source_url: str = ""
    quality_score: int = Field(default=0, ge=0, le=100)
    raw: dict[str, Any] = Field(default_factory=dict, exclude=True)


class SearchRequest(BaseModel):
    provider: ProviderName = ProviderName.sample
    query: str = Field(min_length=2, max_length=120)
    city: str = Field(min_length=2, max_length=120)
    radius_m: int = Field(default=5000, ge=100, le=50000)
    limit: int = Field(default=30, ge=1, le=100)
    language: str = Field(default="en", min_length=2, max_length=10)
    deduplicate: bool = True

    @field_validator("query", "city")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("Value cannot be empty")
        return value


class SearchMeta(BaseModel):
    provider: str
    query: str
    city: str
    returned: int
    duplicates_removed: int = 0
    warnings: list[str] = Field(default_factory=list)
    cache_hit: bool = False
    cache_stale: bool = False
    cache_age_seconds: int | None = Field(default=None, ge=0)


class SearchResponse(BaseModel):
    businesses: list[Business]
    meta: SearchMeta


class ExportRequest(BaseModel):
    businesses: list[Business]


class AnalysisRequest(BaseModel):
    businesses: list[Business] = Field(min_length=1, max_length=100)
    instruction: str = Field(
        default="Summarize market patterns, data gaps, and practical next steps.",
        min_length=5,
        max_length=500,
    )


class AnalysisResponse(BaseModel):
    provider: str
    model: str
    text: str


class ProviderStatus(BaseModel):
    id: str
    label: str
    enabled: bool
    requires_key: bool
    note: str
