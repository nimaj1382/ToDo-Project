from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
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
    status: TaskStatusEnum = Field(default = TaskStatusEnum.TODO, description = "Task status")
    due_date: Optional[datetime] = Field(None, description = "Task due date")


class TaskResponse(TaskBase):
    """Schema for Task response.

    Includes all Task attributes plus the database-generated id and relationships.
    """
    id: int = Field(..., description = "Task ID")
    project_id: int = Field(..., description = "ID of the project this task belongs to")
    closed_at: Optional[datetime] = Field(None, description = "Task closed timestamp")

    model_config = ConfigDict(from_attributes = True)