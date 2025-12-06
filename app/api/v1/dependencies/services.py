from typing import Generator

from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_services import ProjectService
from app.services.task_services import TaskService


def get_db() -> Generator:
    """Dependency for getting database session.

    Yields:
        Database session that is automatically closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db=None) -> ProjectService:
    """Dependency for getting ProjectService.

    Args:
        db: Database session (injected by FastAPI)

    Returns:
        ProjectService instance with repository dependencies.
    """
    if db is None:
        db = next(get_db())
    project_repo = ProjectRepository(db)
    return ProjectService(project_repo)


def get_task_service(db=None) -> TaskService:
    """Dependency for getting TaskService.

    Args:
        db: Database session (injected by FastAPI)

    Returns:
        TaskService instance with repository dependencies.
    """
    if db is None:
        db = next(get_db())
    task_repo = TaskRepository(db)
    return TaskService(task_repo)