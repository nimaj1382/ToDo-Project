from datetime import datetime
from typing import Optional, List, Type, Any

from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus


class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_task_by_id(self, task_id) -> Optional[Task]:
        return self.session.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_name(self, task_name: str) -> list[Type[Task]]:
        return list(self.session.query(Task).filter(Task.name == task_name))

    def add_task(self, task: Task) -> None:
        self.session.add(task)
        self.session.commit()

    def delete_task(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def set_task_name(self, task: Task, new_task_name: str) -> None:
        task.name = new_task_name
        self.session.commit()

    def set_task_description(self, task: Task, new_task_description: str) -> None:
        task.description = new_task_description
        self.session.commit()

    def set_task_status(self, task: Task, new_task_status: TaskStatus) -> None:
        task.status = new_task_status
        self.session.commit()

    def set_task_due_date(self, task: Task, new_task_due_date: datetime) -> None:
        task.due_date = new_task_due_date
        self.session.commit()

    def set_task_project_id(self, task: Task, task_project_id: int):
        task.project_id = task_project_id
        self.session.commit()

    def set_task_closed_at(self, task: Task, closed_at: datetime) -> None:
        task.closed_at = closed_at
        self.session.commit()

    def all_tasks(self) -> list[Type[Task]]:
        return list(self.session.query(Task))