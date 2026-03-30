import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "DevTrack"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = (
        "postgresql+psycopg://postgres.YOUR_PROJECT_REF:YOUR_DB_PASSWORD@"
        "aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
    )
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

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

# Ensure SQLAlchemy uses psycopg dialect when a generic postgres URL is supplied.
if settings.DATABASE_URL.startswith("postgresql://"):
    settings.DATABASE_URL = settings.DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

_PLACEHOLDERS = {
    "YOUR_DB_PASSWORD",
    "YOUR_SUPABASE_PUBLISHABLE_KEY",
    "YOUR_PROJECT_REF",
}

if any(token in settings.DATABASE_URL for token in _PLACEHOLDERS):
    _where = (
        "Vercel → Project → Settings → Environment Variables (Production & Preview)."
        if os.getenv("VERCEL")
        else ".env (local)."
    )
    raise RuntimeError(
        "DATABASE_URL still contains placeholder values. Set the Supabase "
        f"Transaction Pooler URL (user, password, host) in {_where}"
    )

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
