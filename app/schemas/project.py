from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    project_type: str | None = None  # e.g. web-app, mobile-app, website
    role: str | None = None          # fullstack, frontend, backend
    language: str | None = None      # Python, JavaScript, Go …
    framework: str | None = None     # FastAPI, React, Flutter …


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    # Optional fields for partial updates
    name: str | None = None
    description: str | None = None
    project_type: str | None = None
    role: str | None = None
    language: str | None = None
    framework: str | None = None


class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
