from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


# all config values loaded from .env — single source of truth for the app
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gcp_project_id: str
    gcs_bucket_name: str
    vertex_ai_location: str = "us-central1"
    gemini_model_name: str = "gemini-2.5-flash-lite"
    embedding_model_name: str = "models/text-embedding-004"
    api_key: str
    google_api_key: str


# returns the same Settings object every time — reads .env only once at startup
@lru_cache
def get_settings() -> Settings:
    return Settings()
