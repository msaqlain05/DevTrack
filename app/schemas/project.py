from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints

ProjectType = Literal[
    "web-app", "website", "mobile-app", "desktop-app", "api", "cli", "library", "other"
]
ProjectRole = Literal["fullstack", "frontend", "backend"]
ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
OptionalShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
OptionalDescription = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]

class ProjectBase(BaseModel):
    name: ShortText
    description: OptionalDescription | None = None
    project_type: ProjectType | None = None
    role: ProjectRole | None = None
    language: OptionalShortText | None = None
    framework: OptionalShortText | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    # Optional fields for partial updates
    name: ShortText | None = None
    description: OptionalDescription | None = None
    project_type: ProjectType | None = None
    role: ProjectRole | None = None
    language: OptionalShortText | None = None
    framework: OptionalShortText | None = None


class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
