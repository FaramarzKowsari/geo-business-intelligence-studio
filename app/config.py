from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "GeoBusiness Intelligence Studio"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_contact_email: str = (
        "https://github.com/FaramarzKowsari/geo-business-intelligence-studio"
    )
    public_base_url: str = ""
    request_timeout_seconds: float = Field(default=30.0, ge=5.0, le=120.0)

    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    overpass_base_url: str = "https://overpass-api.de/api/interpreter"
    osm_tile_url: str = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    nominatim_min_interval_seconds: float = Field(default=1.1, ge=1.0, le=60.0)
    overpass_min_interval_seconds: float = Field(default=1.0, ge=0.5, le=60.0)
    geocode_cache_ttl_seconds: int = Field(default=604800, ge=3600, le=31536000)
    geocode_stale_ttl_seconds: int = Field(default=2592000, ge=0, le=31536000)
    osm_search_cache_ttl_seconds: int = Field(default=900, ge=60, le=86400)
    osm_search_stale_ttl_seconds: int = Field(default=3600, ge=0, le=604800)
    public_osm_requests_per_minute: int = Field(default=10, ge=1, le=120)
    public_osm_max_records: int = Field(default=50, ge=1, le=100)
    public_osm_max_radius_m: int = Field(default=25000, ge=1000, le=50000)
    public_osm_enabled: bool = True

    google_places_api_key: str = ""
    google_search_cache_ttl_seconds: int = Field(default=300, ge=0, le=86400)

    ai_provider: str = "none"
    ai_model: str = "qwen3:4b"
    ai_base_url: str = "http://localhost:11434/v1"
    ai_api_key: str = ""

    @property
    def user_agent(self) -> str:
        return f"GeoBusinessIntelligenceStudio/1.2 (+{self.app_contact_email})"

    @property
    def is_public_deployment(self) -> bool:
        return self.app_env.casefold() in {"production", "render", "public"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
