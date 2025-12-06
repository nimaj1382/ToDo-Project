import os
import textwrap
from typing import Optional, List, Type
from datetime import datetime

from dotenv import load_dotenv

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

    def get_tasks_by_name(self, task_name: str) -> list[Type[Task]]:
        return self.repository.get_tasks_by_name(task_name)

    def delete_task(self, task: Task) -> None:
        self.repository.delete_task(task)

    def delete_task_by_id(self, task_id: int) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.delete_task(task)

    def set_task_name(self, task: Task, new_task_name: str) -> None:
        # Ensure task name is unique within the project
        tasks_with_same_name = self.get_tasks_by_name(new_task_name)
        for task in tasks_with_same_name:
            if task.project_id == task.project_id:
                raise UniquenessError("Task name within a project "
                                      "must be unique. The given task "
                                      "name for the given project is already in use.")
        self.repository.set_task_name(task, new_task_name)

    def set_task_name_by_id(self, task_id: int, new_task_name: str) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.set_task_name(task, new_task_name)

    def set_task_description(self, task: Task, new_task_description: str) -> None:
        self.repository.set_task_name(task, new_task_description)

    def set_task_description_by_id(self, task_id: int, new_task_description: str) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.set_task_description(task, new_task_description)

    def set_task_status(self, task: Task, task_status: TaskStatus) -> None:
        if not isinstance(task_status, TaskStatus):
            raise ValueError("task_status must be an instance of TaskStatus.")
        self.repository.set_task_status(task, task_status)

    def set_task_status_by_id(self, task_id: int, task_status: TaskStatus) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.set_task_status(task, task_status)

    def set_task_due_date(self, task: Task, task_due_date: datetime) -> None:
        if not isinstance(task_due_date, datetime):
            raise ValueError("task_due_date must be an instance of datetime.")
        self.repository.set_task_due_date(task, task_due_date)

    def set_task_due_date_by_id(self, task_id: int, task_due_date: datetime) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.set_task_due_date(task, task_due_date)

    def set_task_project_id(self, task: Task, task_project_id: int,
                            project_service: 'ProjectService') -> None:
        project = project_service.get_project_by_id(task_project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        # Ensure task name is unique within the destination project
        tasks_with_same_name = self.get_tasks_by_name(task.name)
        for task in tasks_with_same_name:
            if task.project_id == task_project_id:
                raise UniquenessError("Task name within a project "
                                      "must be unique. The given task "
                                      "name for the given project is already in use.")
        self.repository.set_task_project_id(task, task_project_id)

    def set_task_project_id_by_id(self, task_id: int, task_project_id: int,
                                  project_service: 'ProjectService') -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.set_task_project_id(task, task_project_id, project_service)

    def set_task_closed_at(self, task: Task, closed_at: datetime) -> None:
        if not isinstance(closed_at, datetime):
            raise ValueError("closed_at must be an instance of datetime.")
        self.repository.set_task_closed_at(task, closed_at)

    def set_task_closed_at_by_id(self, task_id: int, closed_at: datetime) -> None:
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ExistanceError("task with given id does not exist.")
        self.set_task_closed_at(task, closed_at)

    def all_tasks(self) -> List[Type[Task]]:
        return self.repository.all_tasks()

    def print_all_tasks(self, indent: int = 0) -> None:
        all_tasks = self.all_tasks()
        load_dotenv()
        max_name_length = int(os.getenv("MAX_SHOW_NAME_LENGTH", 10))
        max_description_length = int(os.getenv("MAX_SHOW_DESCRIPTION_LENGTH", 15))
        max_due_date_length = int(os.getenv("MAX_SHOW_DUE_DATE_LENGTH", 10))
        max_closed_at_length = int(os.getenv("MAX_SHOW_CLOSED_AT_LENGTH", 10))
        tab_indent = '\t' * indent
        print(f"{tab_indent}"
              f"{'task id':^15} \t"
              f"|{'task name':^{max_name_length}} \t"
              f"|{'task description':^{max_description_length}} \t"
              f"|{'task status':^10} \t"
              f"|{'task due date':^{max_due_date_length}} \t"
              f"|{'task closed at':^{max_closed_at_length}} \t"
              f"|{'task project id':^15}")
        print()
        for task in all_tasks:
            self.print_task(task, indent)

    def print_task(self, task: Type[Task], indent: int = 0) -> None:
        load_dotenv()
        max_name_length = int(os.getenv("MAX_SHOW_NAME_LENGTH", 10))
        max_description_length = int(os.getenv("MAX_SHOW_DESCRIPTION_LENGTH", 15))
        max_due_date_length = int(os.getenv("MAX_SHOW_DUE_DATE_LENGTH", 10))
        max_closed_at_length = int(os.getenv("MAX_SHOW_CLOSED_AT_LENGTH", 10))
        tab_indent = '\t' * indent

        display_name = (str(task.name)[:max_name_length] +
                        textwrap.shorten(str(task.name)[max_name_length + 1:],
                                         width=3, placeholder="..."))
        display_description = (str(task.description)[:max_description_length] +
                               textwrap.shorten(str(task.description)[max_description_length + 1:],
                                                width=3, placeholder="..."))
        display_due_date = (str(task.due_date)[:max_due_date_length] +
                            textwrap.shorten(str(task.due_date)[max_due_date_length + 1:],
                                             width=3, placeholder="..."))
        display_closed_at = (str(task.closed_at)[:max_closed_at_length] +
                             textwrap.shorten(str(task.closed_at)[max_closed_at_length + 1:],
                                              width=3, placeholder="..."))
        display_closed_at = str(task.closed_at) if task.closed_at else ""
        print(f"{tab_indent}"
              f"{task.id:<15} \t"
              f"|{display_name:<{max_name_length}} \t"
              f"|{display_description:<{max_description_length}} \t"
              f"|{task.status:<10} \t"
              f"|{display_due_date:<{max_due_date_length}} \t"
              f"|{display_closed_at:<{max_closed_at_length}} \t"
              f"|{task.project_id:<15}")
