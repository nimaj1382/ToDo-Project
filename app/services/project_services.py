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
        self.repository.get_project_by_name(project_name)

    def delete_project(self, project: Project) -> None:
        self.repository.delete_project(project)

    def delete_project_by_id(self, project_id: int) -> None:
        self.delete_project(self.get_project_by_id(project_id))

    def delete_project_by_name(self, project_name: str) -> None:
        self.delete_project(self.get_project_by_name(project_name))

    def add_task_to_project(self, project: Project, *,
                            task_name: str,
                            task_description: str = None,
                            task_status: 'TaskStatus' = TaskStatus.TODO,
                            task_due_date: datetime = None,
                            task_project_id: int,
                            task_service: 'TaskService') -> 'Task':

        return task_service.create_task(task_name = task_name,
                                        task_description = task_description,
                                        task_status = task_status,
                                        task_due_date = task_due_date,
                                        task_project_id = project.id)

    def add_task_to_project_by_id(self, project_id: int, *,
                            task_name: str,
                            task_description: str = None,
                            task_status: 'TaskStatus' = TaskStatus.TODO,
                            task_due_date: datetime = None,
                            task_project_id: int,
                            task_service: 'TaskService') -> 'Task':

        return task_service.create_task(task_name=task_name,
                                        task_description=task_description,
                                        task_status=task_status,
                                        task_due_date=task_due_date,
                                        task_project_id=project_id)

    def add_task_to_project_by_name(self, project_name: str, *,
                            task_name: str,
                            task_description: str = None,
                            task_status: 'TaskStatus' = TaskStatus.TODO,
                            task_due_date: datetime = None,
                            task_project_id: int,
                            task_service: 'TaskService') -> 'Task':

        project = self.get_project_by_name(project_name)
        return task_service.create_task(task_name=task_name,
                                        task_description=task_description,
                                        task_status=task_status,
                                        task_due_date=task_due_date,
                                        task_project_id=project.id)

    def project_tasks_list(self, project: Project) -> List['Task']:
        return self.repository.project_tasks_list(project)

    def project_tasks_list_by_id(self, project_id: int) -> List['Task']:
        project = self.get_project_by_id(project_id)
        if project:
            return self.project_tasks_list(project)

    def project_tasks_list_by_name(self, project_name: str) -> Optional[List['Task']]:
        project = self.get_project_by_name(project_name)
        if project:
            return self.project_tasks_list(project)