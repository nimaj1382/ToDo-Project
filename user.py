import os

from dotenv import load_dotenv

from exceptions import MaxLimitExceededError


class User:

    def __init__(self, *, username: str = None, full_name: str = None):
        """
        Initialize a User instance with optional username and full name.
        param username: Optional username for the user.
        param full_name: Optional full name for the user.
        return: None
        """

        self._projects = []
        self._username = None
        self._full_name = None
        if username:
            self.username = username
        if full_name:
            self.full_name = full_name

    @property
    def projects(self):
        return self._projects

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        self._full_name = value

    def add_project(self, project: "Project") -> None:
        """
        Add a Project instance to the user's project list.
        param project: Project instance to be added.
        return: None
        raise MaxLimitExceededError: If adding the project exceeds the maximum limit.
        raise ValueError: If the project name is not unique within the user's projects.
        """

        # Check for limit on number of projects
        load_dotenv()
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 30))
        if len(self.projects) >= max_projects:
            raise MaxLimitExceededError(f"Cannot add more than {max_projects} projects to a user.")
        # Check for uniqueness of project name within user's projects
        for p in self.projects:
            if p.project_name == project.project_name:
                raise ValueError("Project name must be unique within the user's projects.")
        # If the project is already associated with another user, remove it from that user's list
        if project.container_user and project in project.container_user.projects:
            project.container_user.projects.remove(project)
        project._container_user = self
        self.projects.append(project)

    def show_projects(self) -> None:
        """
        Display all projects associated with the user.
        return: None
        """

        # Check if there are any projects
        if len(self.projects) == 0:
            print(f"{self.username} has no projects.")
            return
        # List each project with its name and description
        result_string = f"{self.username}'s Projects:\n"
        for project in self.projects:
            result_string += f"{project.project_name} - {project.project_description}\n"
        print(result_string)

    def remove_user(self) -> None:
        # Delete all projects associated with the user
        for project in self.projects:
            project.delete_project()
        del self

    def number_of_tasks(self) -> int:
        """
        Count the total number of tasks across all projects of the user.
        return: Total number of tasks as an integer.
        """

        total_tasks = 0
        # Iterate through each project and sum the number of tasks
        for project in self.projects:
            total_tasks += len(project.project_tasks)
        return total_tasks

    def show_tasks(self) -> None:
        """
        Display all tasks across all projects of the user.
        return: None
        """

        # Check if there are any tasks
        if self.number_of_tasks() == 0:
            print(f"{self.username} has no tasks across all projects.")
            return
        # List tasks grouped by project
        print(f"{self.username}'s Tasks Across All Projects:")
        for project in self.projects:
            project.show_tasks()

    def __str__(self) -> str:
        return f"User: {self.username} - {self.full_name}"

    def __repr__(self) -> str:
        return self.__str__()
