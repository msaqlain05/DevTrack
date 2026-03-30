import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.env_validator import (
    normalize_database_url,
    sync_auth_secrets,
    validate_env,
)


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "DevTrack"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SQL_ECHO: bool = False

    # Database
    DATABASE_URL: str = (
        "postgresql+psycopg://postgres.YOUR_PROJECT_REF:YOUR_DB_PASSWORD@"
        "aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
    )
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

    # Security (use long random strings in production; min 32 chars on Vercel)
    SECRET_KEY: str = "change-me-in-production"

    # JWT (if left at default, reuses SECRET_KEY after _sync_auth_secrets)
    JWT_SECRET_KEY: str = "change-jwt-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()

settings.DATABASE_URL = normalize_database_url(settings.DATABASE_URL)
settings.SECRET_KEY, settings.JWT_SECRET_KEY = sync_auth_secrets(
    settings.SECRET_KEY, settings.JWT_SECRET_KEY
)
validate_env(
    database_url=settings.DATABASE_URL,
    secret_key=settings.SECRET_KEY,
    jwt_secret_key=settings.JWT_SECRET_KEY,
    vercel=bool(os.getenv("VERCEL")),
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_KEY,
)
