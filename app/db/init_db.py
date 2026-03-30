from sqlalchemy import inspect, text

from app.db.base import Base
from app.db.session import engine

# Import all models here so SQLAlchemy discovers them before creating tables.
from app.models.user import User  # noqa: F401
from app.models.task import Task  # noqa: F401
from app.models.project import Project  # noqa: F401


def _users_table_kwargs(engine) -> dict:
    if engine.dialect.name == "postgresql":
        return {"schema": "public"}
    return {}


def _ensure_users_columns_match_model(engine) -> None:
    """
    Align public.users with the User ORM model.

    Supabase (or a prior partial run) may already define ``users`` without
    ``hashed_password`` / ``created_at``. create_all() does not ALTER tables,
    so we add missing columns idempotently.
    """
    tkw = _users_table_kwargs(engine)
    insp = inspect(engine)
    if not insp.has_table("users", **tkw):
        return
    cols = {c["name"] for c in insp.get_columns("users", **tkw)}
    with engine.begin() as conn:
        if "hashed_password" not in cols:
            conn.execute(
                text(
                    "ALTER TABLE public.users ADD COLUMN IF NOT EXISTS "
                    "hashed_password VARCHAR(255)"
                )
            )
        conn.execute(
            text(
                "UPDATE public.users SET hashed_password = '' "
                "WHERE hashed_password IS NULL"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE public.users ALTER COLUMN hashed_password SET NOT NULL"
            )
        )
        if "created_at" not in cols:
            conn.execute(
                text(
                    "ALTER TABLE public.users ADD COLUMN IF NOT EXISTS created_at "
                    "TIMESTAMPTZ NOT NULL DEFAULT now()"
                )
            )


def init_db() -> None:
    """Create all database tables defined via ORM models."""
    Base.metadata.create_all(bind=engine)
    if engine.dialect.name == "postgresql":
        _ensure_users_columns_match_model(engine)

