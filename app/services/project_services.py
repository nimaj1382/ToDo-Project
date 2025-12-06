import os
import textwrap
from datetime import datetime
from typing import Optional, List, Type
from dotenv import load_dotenv

from app.models.project import Project
from app.models.task import TaskStatus
from app.repositories.project_repository import ProjectRepository
from app.exceptions.service_exceptions import *

class ProjectService:
    """Business logic for managing Project entities.

    Coordinates repository interactions and task-related operations that
    impact projects. Also provides formatted printing helpers for CLI output.

    Attributes:
        repository: The ProjectRepository used for persistence operations.
    """

    def __init__(self, repository: ProjectRepository):
        """Initialize the service with its repository dependency.

        Args:
            repository: ProjectRepository instance.
        """
        self.repository = repository

    def create_project(self, *, project_name: str, project_description: str = None) -> Project:
        """Create a new project after validating inputs.

        Ensures name/description length constraints and uniqueness of name,
        then persists the project via the repository.

        Args:
            project_name: Desired project name (<= 30 chars).
            project_description: Optional description (<= 150 chars).
        Returns:
            The created Project instance.
        Raises:
            MaxLengthExceededError: If name or description exceeds limits.
            UniquenessError: If a project with the same name already exists.
        """

        # Check name and description length
        if len(project_name) > 30:
            raise MaxLengthExceededError("Project name must be 30 characters or fewer.")

        if project_description and len(project_description) > 150:
            raise MaxLengthExceededError("Project description must be 150 characters or fewer")

        # Check uniqueness of project name
        # Note: Using service-level fetch to enforce business rule before creation.
        if self.get_project_by_name(project_name) != None:
            raise UniquenessError("Project name must be unique. "
                                  "The given project name is already in use.")

        project = Project(name = project_name, description = project_description)
        self.repository.add_project(project)
        return project

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by its id.

        Args:
            project_id: Project primary key.
        Returns:
            Project if found, otherwise None.
        """
        return self.repository.get_project_by_id(project_id)

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """Retrieve a project by its exact name.

        Args:
            project_name: The name to match.
        Returns:
            Project if found, otherwise None.
        """
        return self.repository.get_project_by_name(project_name)

    def delete_project(self, project: Project, task_service: 'TaskService') -> None:
        """Delete a project and cascade delete its tasks via TaskService.

        Args:
            project: Project to remove.
            task_service: Service used to delete tasks linked to the project.
        """
        project_tasks = self.project_tasks_list(project)
        for task in project_tasks:
            task_service.delete_task(task)
        self.repository.delete_project(project)

    def delete_project_by_id(self, project_id: int, task_service: 'TaskService') -> None:
        """Delete a project by id, ensuring it exists first.

        Args:
            project_id: Project id to remove.
            task_service: Service used to delete tasks linked to the project.
        Raises:
            ExistanceError: If project does not exist.
        """
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        self.delete_project(project, task_service)

    def delete_project_by_name(self, project_name: str, task_service: 'TaskService') -> None:
        """Delete a project by name, ensuring it exists first.

        Args:
            project_name: Project name to remove.
            task_service: Service used to delete tasks linked to the project.
        Raises:
            ExistanceError: If project does not exist.
        """
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
        """Create and attach a task to the given project.

        Delegates to TaskService.create_task while ensuring the project id is
        passed as the task_project_id.

        Args:
            project: Target project.
            task_name: New task name.
            task_description: Optional task description.
            task_status: Initial status (default TODO).
            task_due_date: Optional due date.
            task_service: Task service dependency.
        Returns:
            The created Task.
        """

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
        """Create and attach a task to the project identified by id.

        Args:
            project_id: Target project id.
            task_name: New task name.
            task_description: Optional task description.
            task_status: Initial status (default TODO).
            task_due_date: Optional due date.
            task_service: Task service dependency.
        Returns:
            The created Task.
        Raises:
            ExistanceError: If the project is missing.
        """

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
        """Create and attach a task to the project identified by name.

        Args:
            project_name: Target project name.
            task_name: New task name.
            task_description: Optional task description.
            task_status: Initial status (default TODO).
            task_due_date: Optional due date.
            task_service: Task service dependency.
        Returns:
            The created Task.
        Raises:
            ExistanceError: If the project is missing.
        """

        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        return self.add_task_to_project(project=project,
                                        task_name=task_name,
                                        task_description=task_description,
                                        task_status=task_status,
                                        task_due_date=task_due_date,
                                        task_service=task_service)

    def project_tasks_list(self, project: Type[Project]) -> List[Type['Task']]:
        """Return tasks belonging to the given project."""
        return self.repository.project_tasks_list(project)

    def project_tasks_list_by_id(self, project_id: int) -> List['Task']:
        """Return tasks belonging to the project identified by id.

        Raises:
            ExistanceError: If the project is missing.
        """
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        return self.project_tasks_list(project)

    def project_tasks_list_by_name(self, project_name: str) -> Optional[List['Task']]:
        """Return tasks belonging to the project identified by name.

        Raises:
            ExistanceError: If the project is missing.
        """
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        return self.project_tasks_list(project)

    def set_project_name(self, project: Project, new_project_name: str) -> None:
        """Update a project's name after uniqueness validation."""
        if self.get_project_by_name(new_project_name):
            raise UniquenessError("Project name must be unique. "
                                  "The given project name is already in use.")
        self.repository.set_project_name(project, new_project_name)

    def set_project_name_by_id(self, project_id: int, new_project_name: str) -> None:
        """Update a project's name by id after existence check."""
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        self.set_project_name(project, new_project_name)

    def set_project_name_by_name(self, project_name: str, new_project_name: str) -> None:
        """Update a project's name by name after existence check."""
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        self.set_project_name(project, new_project_name)

    def set_project_description(self, project: Project, new_project_description: str) -> None:
        """Update a project's description."""
        self.repository.set_project_description(project, new_project_description)

    def set_project_description_by_id(self, project_id: int, new_project_description: str) -> None:
        """Update a project's description by id after existence check."""
        project = self.get_project_by_id(project_id)
        if project is None:
            raise ExistanceError("project with given id does not exist.")
        self.set_project_description(project, new_project_description)

    def set_project_description_by_name(self, project_name: str,
                                        new_project_description: str) -> None:
        """Update a project's description by name after existence check."""
        project = self.get_project_by_name(project_name)
        if project is None:
            raise ExistanceError("project with given name does not exist.")
        self.set_project_description(project, new_project_description)

    def all_projects(self) -> List[Type[Project]]:
        """Return all projects."""
        return self.repository.all_projects()

    def print_all_projects(self, indent:int = 0) -> None:
        """Print a table of all projects.

        Reads environment-based width settings, prints header, and delegates
        row formatting to print_project.
        """
        all_projects = self.all_projects()
        load_dotenv()
        # Read width configuration from environment with defaults.
        max_name_length = int(os.getenv("MAX_SHOW_NAME_LENGTH", 10))
        max_description_length = int(os.getenv("MAX_SHOW_DESCRIPTION_LENGTH", 15))
        tab_indent = '\t' * indent

        print(f"{tab_indent}"
              f"{'project id':^15} \t"
              f"|{'project name':^{max_name_length}} \t"
              f"|{'project description':^{max_description_length}}")
        print()

        for project in all_projects:
            self.print_project(project, indent)

    def print_project(self, project: Type[Project], indent: int = 0) -> None:
        """Print a single project's summary row.

        Applies truncation and ellipsis using textwrap.shorten based on
        environment-configured widths.
        """
        load_dotenv()
        max_name_length = int(os.getenv("MAX_SHOW_NAME_LENGTH", 10))
        max_description_length = int(os.getenv("MAX_SHOW_DESCRIPTION_LENGTH", 15))
        max_due_date_length = int(os.getenv("MAX_SHOW_DUE_DATE_LENGTH", 10))
        tab_indent = '\t' * indent

        # Build display strings: take a prefix slice, then append an ellipsis-shortened suffix.
        display_name = (str(project.name)[:max_name_length] +
                        textwrap.shorten(str(project.name)[max_name_length + 1:],
                                         width=3, placeholder="..."))
        display_description = (str(project.description)[:max_description_length] +
                            textwrap.shorten(str(project.description)[max_description_length + 1:],
                                         width=3, placeholder="..."))
        print(f"{tab_indent}"
              f"{project.id:<15} \t"
              f"|{display_name:<{max_name_length}} \t"
              f"|{display_description:<{max_description_length}}")

    def print_all_projects_with_tasks(self, task_service: 'TaskService', indent: int = 0):
        """Print projects with their tasks underneath each project.

        Prints a header and then, for each project, shows the project row and
        its tasks. A separator line is printed around the task list when present.
        """
        load_dotenv()
        max_name_length = int(os.getenv("MAX_SHOW_NAME_LENGTH", 10))
        max_description_length = int(os.getenv("MAX_SHOW_DESCRIPTION_LENGTH", 15))
        max_due_date_length = int(os.getenv("MAX_SHOW_DUE_DATE_LENGTH", 10))
        tab_indent = '\t' * indent

        all_projects = self.all_projects()

        print(f"{tab_indent}"
              f"{'project id':^15} \t"
              f"|{'project name':^{max_name_length}} \t"
              f"|{'project description':^{max_description_length}}")
        print()

        for project in all_projects:
            self.print_project(project, indent)
            project_tasks = self.project_tasks_list(project)
            if len(project_tasks) > 0:
                # Visual separator sized relative to configured widths.
                print(f"{'tasks':-^{max_name_length + max_description_length + 20}}")
                for task in project_tasks:
                    # Increase indent for tasks to visually nest under project.
                    task_service.print_task(task, indent + 1)
                print(f"{'end of tasks':-^{max_name_length + max_description_length + 20}}")
                print("\n\n")