from app.db.base import Base
from app.db.session import engine

# Import all models here so SQLAlchemy discovers them before creating tables.
from app.models.user import User  # noqa: F401
from app.models.task import Task  # noqa: F401


def init_db() -> None:
    """Create all database tables defined via ORM models."""
    Base.metadata.create_all(bind=engine)

