from typing import Optional
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base schema for Project with shared attributes."""
    name: str = Field(..., max_length=30, description="Project name (max 30 characters)")
    description: Optional[str] = Field(None, max_length=150,
                                       description="Project description (max 150 characters)")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project.

    Validates:
    - name: required, max 30 characters
    - description: optional, max 150 characters
    """
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project.

    All fields are optional to support partial updates.
    """
    name: Optional[str] = Field(None, max_length=30, description="New project name")
    description: Optional[str] = Field(None, max_length=150, description="New project description")