from datetime import date

from pydantic import BaseModel

from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    date: date | None = None
    status: TaskStatus = TaskStatus.pending
    project_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: date | None = None
    status: TaskStatus | None = None


class TaskOut(TaskBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
