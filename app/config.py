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
    app_contact_email: str = "replace-with-your-email@example.com"
    request_timeout_seconds: float = Field(default=30.0, ge=5.0, le=120.0)

    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    overpass_base_url: str = "https://overpass-api.de/api/interpreter"
    google_places_api_key: str = ""

    ai_provider: str = "none"
    ai_model: str = "qwen3:4b"
    ai_base_url: str = "http://localhost:11434/v1"
    ai_api_key: str = ""

    @property
    def user_agent(self) -> str:
        return f"GeoBusinessIntelligenceStudio/1.0 ({self.app_contact_email})"


@lru_cache
def get_settings() -> Settings:
    return Settings()
