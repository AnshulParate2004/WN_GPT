from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Resolve .env relative to this file's location: Backend/app/core/config.py → go up 3 levels → WN_GPT/.env
# config.py lives at Backend/app/core/config.py
# parents[2] = Backend/   ← .env lives HERE
# parents[3] = WN_GPT/    ← fallback
_root = Path(__file__).resolve().parents[2]
_ENV_PATH = _root / ".env" if (_root / ".env").exists() else Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str = "gpt-4o"
    openai_api_version: str = "2024-12-01-preview"

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_secret: str

    # Azure Speech (optional for voice input)
    azure_speech_key: str = ""
    azure_speech_region: str = "centralindia"

    # App
    app_name: str = "WellnessGPT"
    debug: bool = True
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = str(_ENV_PATH)
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
