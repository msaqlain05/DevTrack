from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    @staticmethod
    def create_project(db: Session, schema: ProjectCreate, current_user: User) -> Project:
        project = Project(**schema.model_dump(), owner_id=current_user.id)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_projects(db: Session, current_user: User) -> list[Project]:
        # Scoped strictly to the current user
        return db.query(Project).filter(Project.owner_id == current_user.id).all()

    @staticmethod
    def get_project_by_id(db: Session, project_id: int, current_user: User) -> Project:
        project = (
            db.query(Project)
            .filter(Project.id == project_id, Project.owner_id == current_user.id)
            .first()
        )
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        return project

    @staticmethod
    def update_project(
        db: Session, project_id: int, schema: ProjectUpdate, current_user: User
    ) -> Project:
        project = ProjectService.get_project_by_id(db, project_id, current_user)

        # Update only fields that were set
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)

        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete_project(db: Session, project_id: int, current_user: User) -> None:
        project = ProjectService.get_project_by_id(db, project_id, current_user)
        db.delete(project)
        db.commit()
