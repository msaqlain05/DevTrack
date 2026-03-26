import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "DevTrack"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./app/db/devtrack.db"

    # Security
    SECRET_KEY: str = "change-me-in-production"

    # JWT
    JWT_SECRET_KEY: str = "change-jwt-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()

# Vercel serverless functions have a read-only filesystem except /tmp.
if os.getenv("VERCEL") and settings.DATABASE_URL == "sqlite:///./app/db/devtrack.db":
    settings.DATABASE_URL = "sqlite:////tmp/devtrack.db"

_INSECURE_DEFAULTS = {
    "change-me-in-production",
    "change-jwt-secret-in-production",
}

if os.getenv("VERCEL"):
    if settings.SECRET_KEY in _INSECURE_DEFAULTS or len(settings.SECRET_KEY) < 32:
        raise RuntimeError(
            "Insecure SECRET_KEY. Set a strong SECRET_KEY in Vercel environment variables."
        )
    if settings.JWT_SECRET_KEY in _INSECURE_DEFAULTS or len(settings.JWT_SECRET_KEY) < 32:
        raise RuntimeError(
            "Insecure JWT_SECRET_KEY. Set a strong JWT_SECRET_KEY in Vercel environment variables."
        )
