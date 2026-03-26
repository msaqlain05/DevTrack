from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import verify_resource_owner
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.project_service import ProjectService


class TaskService:
    @staticmethod
    def create_task(db: Session, schema: TaskCreate, current_user: User) -> Task:
        # Verify the user actually owns the project they are adding the task to
        ProjectService.get_project_by_id(db, schema.project_id, current_user)

        task = Task(
            **schema.model_dump(exclude={"status"}),
            status=schema.status.value,
            owner_id=current_user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks_by_project(
        db: Session, project_id: int, current_user: User, filter_date: date | None = None
    ) -> list[Task]:
        # Verify the user actually owns the project they are querying
        ProjectService.get_project_by_id(db, project_id, current_user)

        query = db.query(Task).filter(Task.project_id == project_id)
        if filter_date:
            query = query.filter(Task.date == filter_date)

        return query.all()

    @staticmethod
    def get_all_tasks(
        db: Session, current_user: User, filter_date: date | None = None
    ) -> list[Task]:
        """Fetch all tasks owned by user across all projects."""
        query = db.query(Task).filter(Task.owner_id == current_user.id)
        if filter_date:
            query = query.filter(Task.date == filter_date)
        return query.all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, current_user: User) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        verify_resource_owner(task.owner_id, current_user.id)
        return task

    @staticmethod
    def update_task(
        db: Session, task_id: int, schema: TaskUpdate, current_user: User
    ) -> Task:
        task = TaskService.get_task_by_id(db, task_id, current_user)

        update_data = schema.model_dump(exclude_unset=True)
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
            
        for key, value in update_data.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, current_user: User) -> None:
        task = TaskService.get_task_by_id(db, task_id, current_user)
        db.delete(task)
        db.commit()
