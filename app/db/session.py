import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings


def _create_engine():
    """
    Serverless (Vercel): avoid pooled connections across cold starts; use NullPool.

    Supabase transaction pooler (PgBouncer) is incompatible with prepared statements
    in transaction mode — psycopg3 must use ``prepare_threshold=None``.
    """
    kwargs: dict = {"echo": settings.DEBUG}
    connect_args: dict = {}

    if settings.DATABASE_URL.startswith("postgresql"):
        connect_args["prepare_threshold"] = None

    if os.getenv("VERCEL"):
        kwargs["poolclass"] = NullPool
        kwargs["pool_pre_ping"] = True

    if connect_args:
        kwargs["connect_args"] = connect_args

    return create_engine(settings.DATABASE_URL, **kwargs)


engine = _create_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    FastAPI dependency that provides a database session per request.
    Ensures the session is always closed, even on exceptions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
