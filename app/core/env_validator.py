import os
from urllib.parse import urlparse


INSECURE_DEFAULTS = frozenset(
    {
        "change-me-in-production",
        "change-jwt-secret-in-production",
    }
)

PLACEHOLDERS = {
    "YOUR_DB_PASSWORD",
    "YOUR_SUPABASE_PUBLISHABLE_KEY",
    "YOUR_PROJECT_REF",
}


def is_strong_secret(value: str) -> bool:
    return value not in INSECURE_DEFAULTS and len(value) >= 32


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def sync_auth_secrets(secret_key: str, jwt_secret_key: str) -> tuple[str, str]:
    sec_strong = is_strong_secret(secret_key)
    jwt_strong = is_strong_secret(jwt_secret_key)
    if sec_strong and not jwt_strong:
        return secret_key, secret_key
    if jwt_strong and not sec_strong:
        return jwt_secret_key, jwt_secret_key
    return secret_key, jwt_secret_key


def _describe_secret_env(name: str) -> str:
    """Privacy-safe hint: unset vs empty vs too short vs default placeholder."""
    raw = os.environ.get(name)
    if raw is None:
        return f"{name}: not present in process environment (Vercel did not inject it for this deployment)."
    stripped = raw.strip()
    if not stripped:
        return f"{name}: set but empty."
    if stripped in INSECURE_DEFAULTS:
        return f"{name}: still the dev placeholder — replace with a random value (>=32 chars)."
    if len(stripped) < 32:
        return f"{name}: length is {len(stripped)} — must be >= 32 characters."
    return f"{name}: OK (length {len(stripped)})."


def validate_env(
    *,
    database_url: str,
    secret_key: str,
    jwt_secret_key: str,
    vercel: bool,
    supabase_url: str | None = None,
    supabase_key: str | None = None,
) -> None:
    errors: list[str] = []

    if not database_url:
        errors.append("DATABASE_URL is missing.")
    else:
        if any(token in database_url for token in PLACEHOLDERS):
            errors.append(
                "DATABASE_URL contains placeholder values. Set full Supabase "
                "pooler URL (host, username, password, db, sslmode)."
            )
        parsed = urlparse(database_url)
        if not parsed.scheme or not parsed.netloc:
            errors.append("DATABASE_URL is invalid. Expected a full Postgres URL.")

    if vercel and (not is_strong_secret(secret_key) or not is_strong_secret(jwt_secret_key)):
        errors.append(
            "After loading env, SECRET_KEY and JWT_SECRET_KEY must both be strong "
            "(>=32 chars, not dev defaults). Set at least one of SECRET_KEY or "
            "JWT_SECRET_KEY in Vercel; the other is copied automatically."
        )
        errors.append(_describe_secret_env("SECRET_KEY"))
        errors.append(_describe_secret_env("JWT_SECRET_KEY"))
        errors.append(
            "In Vercel, open Environment Variables and enable the key for the "
            "environment you deploy to (Production vs Preview). Redeploy after saving."
        )

    if supabase_url and not supabase_url.startswith(("https://", "http://")):
        errors.append("SUPABASE_URL must start with http:// or https://.")

    if supabase_key and not supabase_key.startswith(("sb_", "eyJ")):
        errors.append("SUPABASE_KEY format looks invalid (expected Supabase anon/service key).")

    if errors:
        where = (
            "Vercel -> Project -> Settings -> Environment Variables"
            if vercel
            else "local .env file"
        )
        raise RuntimeError(
            "Environment validation failed:\n- "
            + "\n- ".join(errors)
            + f"\nFix these values in {where}."
        )

