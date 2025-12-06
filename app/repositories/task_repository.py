from datetime import datetime
from typing import Optional, List, Type, Any

from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus

class TaskRepository:
    """Repository encapsulating database operations for Task.

    Attributes:
        session: Active SQLAlchemy session used for queries and commits.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session.

        Args:
            session: SQLAlchemy Session instance.
        """
        self.session = session

    def get_task_by_id(self, task_id) -> Optional[Task]:
        """Fetch a single task by its primary key.

        Args:
            task_id: Task identifier.
        Returns:
            The Task instance if found; otherwise None.
        """
        return self.session.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_name(self, task_name: str) -> list[Type[Task]]:
        """Fetch tasks matching an exact name.

        Args:
            task_name: Name to match.
        Returns:
            A list of Task objects with the given name.
        """
        return list(self.session.query(Task).filter(Task.name == task_name))

    def add_task(self, task: Task) -> None:
        """Persist a new task.

        Args:
            task: Task instance to add.
        """
        self.session.add(task)
        self.session.commit()

    def delete_task(self, task: Task) -> None:
        """Delete an existing task.

        Args:
            task: Task instance to delete.
        """
        self.session.delete(task)
        self.session.commit()

    def set_task_name(self, task: Task, new_task_name: str) -> None:
        """Update task name and commit.

        Args:
            task: Task to update.
            new_task_name: New name value.
        """
        task.name = new_task_name
        self.session.commit()

    def set_task_description(self, task: Task, new_task_description: str) -> None:
        """Update task description and commit.

        Args:
            task: Task to update.
            new_task_description: New description value.
        """
        task.description = new_task_description
        self.session.commit()

    def set_task_status(self, task: Task, new_task_status: TaskStatus) -> None:
        """Update task status and commit.

        Args:
            task: Task to update.
            new_task_status: New TaskStatus value.
        """
        task.status = new_task_status
        self.session.commit()

    def set_task_due_date(self, task: Task, new_task_due_date: datetime) -> None:
        """Update task due date and commit.

        Args:
            task: Task to update.
            new_task_due_date: New due date as datetime.
        """
        task.due_date = new_task_due_date
        self.session.commit()

    def set_task_project_id(self, task: Task, task_project_id: int):
        """Update related project id and commit.

        Args:
            task: Task to update.
            task_project_id: New project id.
        """
        task.project_id = task_project_id
        self.session.commit()

    def set_task_closed_at(self, task: Task, closed_at: datetime) -> None:
        """Update closed_at timestamp and commit.

        Args:
            task: Task to update.
            closed_at: Closure datetime or None.
        """
        task.closed_at = closed_at
        self.session.commit()

    def all_tasks(self) -> list[Type[Task]]:
        """Return all tasks.

        Returns:
            A list of all Task objects.
        """
        return list(self.session.query(Task))