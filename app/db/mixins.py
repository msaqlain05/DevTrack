from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class OwnerMixin:
    """
    SQLAlchemy model mixin that adds a `user_id` column as a foreign key to the users table.
    Ensures that any model inheriting from this mixin is robustly tied to a specific user.
    """

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
        )
