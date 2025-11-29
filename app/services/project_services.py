from datetime import datetime
from typing import Optional, List

from app.models.project import Project
from app.models.task import TaskStatus
from app.repositories.project_repository import ProjectRepository
from app.exceptions.service_exceptions import *

class ProjectService:

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create_project(self, *, project_name: str, project_description: str = None) -> Project:

        # Check name and description length

        if len(project_name) > 30:
            raise MaxLengthExceededError("Project name must be 30 characters or fewer.")

        if project_description and len(project_description) > 150:
            raise MaxLengthExceededError("Project description must be 150 characters or fewer")

        # Check uniqueness of project name

        if self.get_project_by_name(project_name) != None:
            raise UniquenessError("Project name must be unique. The given project name is already in use.")

        project = Project(name = project_name, description = project_description)
        self.repository.add_project(project)
        return project

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.repository.get_project_by_id(project_id)

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        return self.repository.get_project_by_name(project_name)

    def delete_project(self, project: Project, task_service: 'TaskService') -> None:
        project_tasks = self.project_tasks_list(project)
        for task in project_tasks:
            task_service.delete_task(task)
        self.repository.delete_project(project)

    def delete_project_by_id(self, project_id: int, task_service: 'TaskService') -> None:
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        self.delete_project(project, task_service)

    def delete_project_by_name(self, project_name: str, task_service: 'TaskService') -> None:
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        self.delete_project(project, task_service)

    def add_task_to_project(self, project: Project, *,
                            task_name: str,
                            task_description: str = None,
                            task_status: 'TaskStatus' = TaskStatus.TODO,
                            task_due_date: datetime = None,
                            task_service: 'TaskService') -> 'Task':

        return task_service.create_task(task_name = task_name,
                                        task_description = task_description,
                                        task_status = task_status,
                                        task_due_date = task_due_date,
                                        task_project_id = project.id,
                                        project_service = self)

    def add_task_to_project_by_id(self, project_id: int, *,
                            task_name: str,
                            task_description: str = None,
                            task_status: 'TaskStatus' = TaskStatus.TODO,
                            task_due_date: datetime = None,
                            task_service: 'TaskService') -> 'Task':

        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        return self.add_task_to_project(project = project,
                                        task_name = task_name,
                                        task_description = task_description,
                                        task_status = task_status,
                                        task_due_date = task_due_date,
                                        task_service = task_service)

    def add_task_to_project_by_name(self, project_name: str, *,
                            task_name: str,
                            task_description: str = None,
                            task_status: 'TaskStatus' = TaskStatus.TODO,
                            task_due_date: datetime = None,
                            task_service: 'TaskService') -> 'Task':

        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        return self.add_task_to_project(project=project,
                                        task_name=task_name,
                                        task_description=task_description,
                                        task_status=task_status,
                                        task_due_date=task_due_date,
                                        task_service=task_service)

    def project_tasks_list(self, project: Project) -> List['Task']:
        return self.repository.project_tasks_list(project)

    def project_tasks_list_by_id(self, project_id: int) -> List['Task']:
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        return self.project_tasks_list(project)

    def project_tasks_list_by_name(self, project_name: str) -> Optional[List['Task']]:
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        return self.project_tasks_list(project)

    def set_project_name(self, project: Project, new_project_name: str) -> None:
        if self.get_project_by_name(new_project_name):
            raise UniquenessError("Project name must be unique. The given project name is already in use.")
        self.repository.set_project_name(project, new_project_name)

    def set_project_name_by_id(self, project_id: int, new_project_name: str) -> None:
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        self.set_project_name(project, new_project_name)

    def set_project_name_by_name(self, project_name: str, new_project_name: str) -> None:
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        self.set_project_name(project, new_project_name)

    def set_project_description(self, project: Project, new_project_description: str) -> None:
        self.repository.set_project_description(project, new_project_description)

    def set_project_description_by_id(self, project_id: int, new_project_description: str) -> None:
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        self.set_project_description(project, new_project_description)

    def set_project_description_by_name(self, project_name: str, new_project_description: str) -> None:
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        self.set_project_description(project, new_project_description)