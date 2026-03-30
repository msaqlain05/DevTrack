from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def normalize_email(email: str) -> str:
    """Canonical form for storage, lookups, and JWT ``sub`` (strip + lowercase)."""
    return email.strip().lower()


# ── Password hashing ─────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if *plain* matches *hashed*."""
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except ValueError:
        # Treat malformed hashes as invalid credentials, not server errors.
        return False


# ── JWT ───────────────────────────────────────────────────────────────────────
def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT.

    The caller should put identifying data (e.g. ``{"sub": user.email}``) in
    *data*; an ``exp`` claim is added automatically.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["exp"] = expire
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT.

    Raises
    ------
    jose.JWTError
        If the token is invalid or expired. Callers should catch this and raise
        an appropriate HTTP error.
    """
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
