import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_DEFAULTS = frozenset(
    {
        "change-me-in-production",
        "change-jwt-secret-in-production",
    }
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


def _is_strong_secret(value: str) -> bool:
    return value not in _INSECURE_DEFAULTS and len(value) >= 32


def _sync_auth_secrets(s: Settings) -> None:
    """
    On Vercel, set one strong variable (SECRET_KEY or JWT_SECRET_KEY) and the
    other can stay unset — mirror the strong value so JWT and sessions match.
    """
    sec_strong = _is_strong_secret(s.SECRET_KEY)
    jwt_strong = _is_strong_secret(s.JWT_SECRET_KEY)
    if sec_strong and not jwt_strong:
        s.JWT_SECRET_KEY = s.SECRET_KEY
    elif jwt_strong and not sec_strong:
        s.SECRET_KEY = s.JWT_SECRET_KEY


settings = Settings()

# Ensure SQLAlchemy uses psycopg dialect when a generic postgres URL is supplied.
if settings.DATABASE_URL.startswith("postgresql://"):
    settings.DATABASE_URL = settings.DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

_sync_auth_secrets(settings)

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

if os.getenv("VERCEL"):
    if not _is_strong_secret(settings.SECRET_KEY) or not _is_strong_secret(
        settings.JWT_SECRET_KEY
    ):
        raise RuntimeError(
            "Set at least one strong secret (≥32 characters, not the dev defaults) in "
            "Vercel → Settings → Environment Variables: use SECRET_KEY, or JWT_SECRET_KEY, "
            "or both. If you set only one, the other is derived automatically."
        )
