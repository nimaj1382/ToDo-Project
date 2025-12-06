from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatusEnum(str, Enum):
    """Task status enumeration for API."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskBase(BaseModel):
    """Base schema for Task with shared attributes."""
    name: str = Field(..., max_length = 30, description = "Task name (max 30 characters)")
    description: Optional[str] = Field(None, max_length = 150,
                                       description = "Task description (max 150 characters)")
    status: TaskStatusEnum = Field(default=TaskStatusEnum.TODO, description = "Task status")
    due_date: Optional[datetime] = Field(None, description = "Task due date")


class TaskCreate(TaskBase):
    """Schema for creating a new task.

    Validates:
    - name: required, max 30 characters
    - description: optional, max 150 characters
    - status: defaults to TODO
    - due_date: optional datetime
    - project_id: required, must reference an existing project
    """
    project_id: int = Field(..., description = "ID of the project this task belongs to")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional to support partial updates.
    """
    name: Optional[str] = Field(None, max_length = 30, description = "New task name")
    description: Optional[str] = Field(None, max_length = 150, description = "New task description")
    status: Optional[TaskStatusEnum] = Field(None, description = "New task status")
    due_date: Optional[datetime] = Field(None, description = "New task due date")
    closed_at: Optional[datetime] = Field(None, description = "Task closed timestamp")
    project_id: Optional[int] = Field(None, description = "New project ID for the task")