from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task under a specific project strictly owned by the user."""
    return TaskService.create_task(db, payload, current_user)


@router.get("/project/{project_id}", response_model=list[TaskOut])
def list_tasks_by_project(
    project_id: int,
    filter_date: date | None = Query(None, alias="date"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get tasks for a specific project with optional date filtering."""
    return TaskService.get_tasks_by_project(db, project_id, current_user, filter_date)


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    filter_date: date | None = Query(None, alias="date"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all tasks owned by user across all projects with optional date filtering."""
    return TaskService.get_all_tasks(db, current_user, filter_date)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task's status or other fields."""
    return TaskService.update_task(db, task_id, payload, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task owned by the user."""
    TaskService.delete_task(db, task_id, current_user)
