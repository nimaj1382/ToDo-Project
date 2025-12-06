from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.services import get_db, get_project_service, get_task_service
from app.api.v1.schemas.requests.task import TaskCreate, TaskUpdate
from app.api.v1.schemas.responses.task import TaskResponse
from app.services.project_services import ProjectService
from app.services.task_services import TaskService
from app.models.task import TaskStatus
from app.exceptions.service_exceptions import *
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List all tasks",
    description="Retrieve a list of all tasks in the system."
)
async def list_tasks(
        db: Session = Depends(get_db)
) -> List[TaskResponse]:
    """List all tasks.

    Args:
        db: Database session

    Returns:
        List of all tasks with their information.
    """
    task_service = get_task_service(db)
    tasks = task_service.all_tasks()
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task within a project."
)
async def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db)
) -> TaskResponse:
    """Create a new task.

    Args:
        task: Task data (name, description, status, due_date, project_id)
        db: Database session

    Returns:
        The created task with its generated ID.

    Raises:
        HTTPException: 400 if validation fails, 404 if project not found
    """
    task_service = get_task_service(db)
    project_service = get_project_service(db)

    try:
        # Convert string status to TaskStatus enum
        task_status = TaskStatus[task.status.name]

        created_task = task_service.create_task(
            task_name=task.name,
            task_description=task.description,
            task_status=task_status,
            task_due_date=task.due_date,
            task_project_id=task.project_id,
            project_service=project_service
        )
        return TaskResponse.model_validate(created_task)
    except UniquenessError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except MaxLengthExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ExistanceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Retrieve a specific task by its ID."
)
async def get_task(
        task_id: int,
        db: Session = Depends(get_db)
) -> TaskResponse:
    """Get a task by ID.

    Args:
        task_id: The task ID
        db: Database session

    Returns:
        The task with the specified ID.

    Raises:
        HTTPException: 404 if task not found
    """
    task_service = get_task_service(db)
    task = task_service.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update a task's properties."
)
async def update_task(
        task_id: int,
        task_update: TaskUpdate,
        db: Session = Depends(get_db)
) -> TaskResponse:
    """Update a task.

    Args:
        task_id: The task ID to update
        task_update: Fields to update
        db: Database session

    Returns:
        The updated task.

    Raises:
        HTTPException: 404 if task not found, 400 if validation fails
    """
    task_service = get_task_service(db)
    project_service = get_project_service(db)

    try:
        # Check if task exists
        task = task_service.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )

        # Update name if provided
        if task_update.name is not None:
            task_service.set_task_name_by_id(task_id, task_update.name)

        # Update description if provided
        if task_update.description is not None:
            task_service.set_task_description_by_id(task_id, task_update.description)

        # Update status if provided
        if task_update.status is not None:
            task_status = TaskStatus[task_update.status.name]
            task_service.set_task_status_by_id(task_id, task_status)

        # Update due_date if provided
        if task_update.due_date is not None:
            task_service.set_task_due_date_by_id(task_id, task_update.due_date)

        # Update closed_at if provided
        if task_update.closed_at is not None:
            task_service.set_task_closed_at_by_id(task_id, task_update.closed_at)

        # Update project_id if provided
        if task_update.project_id is not None:
            task_service.set_task_project_id_by_id(
                task_id,
                task_update.project_id,
                project_service
            )

        # Fetch updated task
        updated_task = task_service.get_task_by_id(task_id)
        return TaskResponse.model_validate(updated_task)

    except UniquenessError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except MaxLengthExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ExistanceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a specific task."
)
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
) -> None:
    """Delete a task.

    Args:
        task_id: The task ID to delete
        db: Database session

    Raises:
        HTTPException: 404 if task not found
    """
    task_service = get_task_service(db)

    try:
        task_service.delete_task_by_id(task_id)
    except ExistanceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )