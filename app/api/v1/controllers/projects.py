from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.services import get_db, get_project_service, get_task_service
from app.api.v1.schemas.requests.project import ProjectCreate, ProjectUpdate
from app.api.v1.schemas.responses.project import ProjectResponse, TaskResponse
from app.services.project_services import ProjectService
from app.services.task_services import TaskService
from app.exceptions.service_exceptions import *
router = APIRouter(
    prefix = "/projects",
    tags = ["projects"],
)


@router.get(
    "/",
    response_model = List[ProjectResponse],
    summary = "List all projects",
    description = "Retrieve a list of all projects in the system."
)
async def list_projects(
        db: Session = Depends(get_db)
) -> List[ProjectResponse]:
    """List all projects.

    Returns:
        List of all projects with their basic information.
    """
    project_service = get_project_service(db)
    projects = project_service.all_projects()
    return [ProjectResponse.model_validate(project) for project in projects]


@router.post(
    "/",
    response_model = ProjectResponse,
    status_code = status.HTTP_201_CREATED,
    summary = "Create a new project",
    description = "Create a new project with a unique name and optional description."
)
async def create_project(
        project: ProjectCreate,
        db: Session = Depends(get_db)
) -> ProjectResponse:
    """Create a new project.

    Args:
        project: Project data (name and description)
        db: Database session

    Returns:
        The created project with its generated ID.

    Raises:
        HTTPException: 400 if name already exists or validation fails
    """
    project_service = get_project_service(db)

    try:
        created_project = project_service.create_project(
            project_name = project.name,
            project_description = project.description
        )
        return ProjectResponse.model_validate(created_project)
    except UniquenessError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )
    except MaxLengthExceededError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )


@router.get(
    "/{project_id}",
    response_model = ProjectResponse,
    summary = "Get a project by ID",
    description = "Retrieve a specific project by its ID."
)
async def get_project(
        project_id: int,
        db: Session = Depends(get_db)
) -> ProjectResponse:
    """Get a project by ID.

    Args:
        project_id: The project ID
        db: Database session

    Returns:
        The project with the specified ID.

    Raises:
        HTTPException: 404 if project not found
    """
    project_service = get_project_service(db)
    project = project_service.get_project_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Project with id {project_id} not found"
        )

    return ProjectResponse.model_validate(project)


@router.put(
    "/{project_id}",
    response_model = ProjectResponse,
    summary = "Update a project",
    description = "Update a project's name and/or description."
)
async def update_project(
        project_id: int,
        project_update: ProjectUpdate,
        db: Session = Depends(get_db)
) -> ProjectResponse:
    """Update a project.

    Args:
        project_id: The project ID to update
        project_update: Fields to update (name and/or description)
        db: Database session

    Returns:
        The updated project.

    Raises:
        HTTPException: 404 if project not found, 400 if validation fails
        HTTPException: 400 if name already exists or validation fails
        HTTPException: 400 if max length exceeded
    """
    project_service = get_project_service(db)

    try:
        # Check if project exists
        project = project_service.get_project_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Project with id {project_id} not found"
            )

        # Update name if provided
        if project_update.name is not None:
            project_service.set_project_name_by_id(project_id, project_update.name)

        # Update description if provided
        if project_update.description is not None:
            project_service.set_project_description_by_id(project_id, project_update.description)

        # Fetch updated project
        updated_project = project_service.get_project_by_id(project_id)
        return ProjectResponse.model_validate(updated_project)

    except ExistanceError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )
    except UniquenessError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )
    except MaxLengthExceededError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )


@router.delete(
    "/{project_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Delete a project",
    description = "Delete a project and all its associated tasks."
)
async def delete_project(
        project_id: int,
        db: Session = Depends(get_db)
) -> None:
    """Delete a project.

    Args:
        project_id: The project ID to delete
        db: Database session

    Raises:
        HTTPException: 404 if project not found
    """
    project_service = get_project_service(db)
    task_service = get_task_service(db)

    try:
        project_service.delete_project_by_id(project_id, task_service)
    except ExistanceError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )


@router.get(
    "/{project_id}/tasks",
    response_model = List[TaskResponse],
    summary = "List tasks for a project",
    description = "Retrieve all tasks associated with a specific project."
)
async def list_project_tasks(
        project_id: int,
        db: Session = Depends(get_db)
) -> List[TaskResponse]:
    """List all tasks for a project.

    Args:
        project_id: The project ID
        db: Database session

    Returns:
        List of tasks belonging to the project.

    Raises:
        HTTPException: 404 if project not found
    """
    project_service = get_project_service(db)

    try:
        tasks = project_service.project_tasks_list_by_id(project_id)
        return [TaskResponse.model_validate(task) for task in tasks]
    except ExistanceError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(e)
        )