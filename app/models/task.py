from datetime import date
from enum import Enum

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default=TaskStatus.pending.value, nullable=False)
    
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} project_id={self.project_id}>"
