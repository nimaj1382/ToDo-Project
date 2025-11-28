from typing import Optional, List
from datetime import datetime

from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.exceptions.service_exceptions import *
from app.services.project_services import ProjectService


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, *, task_name: str,
                    task_description: str = None,
                    task_status: TaskStatus = TaskStatus.TODO,
                    task_due_date: datetime = None,
                    task_project_id: int,
                    project_service: 'ProjectService') -> Task:

        # Check task name and description length

        if len(task_name) > 30:
            raise MaxLengthExceededError("Task name must be 30 characters or fewer.")

        if task_description and len(task_description) > 150:
            raise MaxLengthExceededError("Task description must be 150 characters or fewer")

        # Check uniqueness of task name

        tasks_with_same_name = self.get_tasks_by_name(task_name)
        for task in tasks_with_same_name:
            if task.project_id == task_project_id :
                raise UniquenessError("Task name within a project "
                                      "must be unique. The given task "
                                      "name for the given project is already in use.")

        # Ensure task_status is of the allowed instance

        if not isinstance(task_status, TaskStatus):
            raise ValueError("task_status must be an instance of TaskStatus.")

        # Ensure task_due_date is an instance of datetime

        if task_due_date and not isinstance(task_due_date, datetime):
            raise ValueError("task_due_date must be an instance of datetime.")

        # Ensure that project id is valid

        if project_service.get_project_by_id(project_id = task_project_id) is None:
            raise ExistanceError("task_project_id is not valid. "
                                 "There is no project with the given id.")

        task = Task(name = task_name, description = task_description,
                    status = task_status, due_date = task_due_date,
                    project_id = task_project_id)
        self.repository.add_task(task)
        return task

    def get_task_by_id(self, task_id: int) -> Task:
        return self.repository.get_task_by_id(task_id)

    def get_tasks_by_name(self, task_name: str) -> List[Task]:
        return self.repository.get_tasks_by_name(task_name)

    def delete_task(self, task: Task) -> None:
        self.repository.delete_task(task)

    def delete_task_by_id(self, task_id: int) -> None:
        self.delete_task(self.get_task_by_id(task_id))

    def set_task_name(self, task: Task, new_task_name: str) -> None:
        self.repository.set_task_name(task, new_task_name)

    def set_task_name_by_id(self, task_id: int, new_task_name: str) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
