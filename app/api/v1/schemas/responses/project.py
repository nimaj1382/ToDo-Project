from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    from app.api.v1.schemas.responses.task import TaskResponse


class ProjectBase(BaseModel):
    """Base schema for Project with shared attributes."""
    name: str = Field(..., max_length = 30, description = "Project name (max 30 characters)")
    description: Optional[str] = Field(None, max_length = 150,
                                       description = "Project description (max 150 characters)")


class ProjectResponse(ProjectBase):
    """Schema for Project response.

    Includes all Project attributes plus the database-generated id.
    """
    id: int = Field(..., description = "Project ID")

    model_config = ConfigDict(from_attributes = True)


class ProjectWithTasksResponse(ProjectResponse):
    """Schema for Project response including its tasks."""
    tasks: list["TaskResponse"] = Field(default_factory = list,
                                        description = "List of tasks in this project")

    model_config = ConfigDict(from_attributes = True)