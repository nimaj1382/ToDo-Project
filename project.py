import os

from dotenv import load_dotenv

from user import User

from task import Task

from exceptions import MaxLimitExceededError



class Project:

    def __init__(self, project_name: str = None, project_description: str = None,
                 container_user: "User" = None):
        """
        Initialize a Project instance with optional name, description, and associated user.
        param project_name: Optional name for the project.
        param project_description: Optional description for the project.
        param container_user: Optional User instance to associate with the project.
        return: None
        raise ValueError: If project_name is not unique within the user's projects.
        raise ValueError: If project_name exceeds 30 characters.
        raise ValueError: If project_description exceeds 150 characters.
        raise ValueError: If container_user is not a User instance.
        """
        self._project_name = None
        self._project_description = None
        self._project_tasks = []
        self._container_user = None

        if project_name:
            self.project_name = project_name
        if project_description:
            self.project_description = project_description
        if container_user:
            self.container_user = container_user

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value: str) -> None:
        # Ensure project name is unique within the user's projects
        if self._container_user:
            for project in self._container_user.projects:
                if project.project_name == value and project != self:
                    raise ValueError("Project name must be unique within the user's projects.")
        # Ensure project name length does not exceed the limit
        if len(value) > 30:
            raise ValueError("Project name must be 30 characters or fewer.")
        self._project_name = value

    @property
    def project_description(self):
        return self._project_description

    @project_description.setter
    def project_description(self, value: str) -> None:
        # Ensure project description length does not exceed the limit
        if len(value) > 150:
            raise ValueError("Project description must be 150 characters or fewer.")
        self._project_description = value

    @property
    def project_tasks(self):
        return self._project_tasks

    @property
    def container_user(self):
        return self._container_user

    @container_user.setter
    def container_user(self, value: "User") -> None:
        # Ensure the value is a User instance
        if not isinstance(value, User):
            raise ValueError("container_user must be a User instance.")
        value.add_project(self)
        # Remove from previous user's project list if applicable
        if self._container_user:
            if self in self._container_user.projects:
                self._container_user.projects.remove(self)
        self._container_user = value


    def set_name(self, new_name: str) -> None:
        self.project_name = new_name

    def set_description(self, new_description: str) -> None:
        self.project_description = new_description

    def delete_project(self):
        # Delete all tasks associated with the project
        for task in self.project_tasks:
            task.delete_task()
        # Remove the project from the user's project list
        if self.container_user and self in self.container_user.projects:
            self.container_user.projects.remove(self)
        del self

    def add_task(self, task: "Task") -> None:
        """
        Add a Task instance to the project's task list.
        param task: Task instance to be added.
        return: None
        raise ValueError: If the task is not a Task instance.
        raise MaxLimitExceededError: If adding the task exceeds the maximum limit.
        raise ValueError: If the task is already in the project's task list.
        """

        # Check if the task is a Task instance
        if not isinstance(task, Task):
            raise ValueError("Only Task instances can be added.")
        # Check if the task is already in the project's task list
        if task in self.project_tasks:
            raise ValueError("Task is already in the project's task list.")
        # Check for limit on number of tasks
        load_dotenv()
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASKS", 20))
        if len(self.project_tasks) >= max_tasks:
            raise MaxLimitExceededError(f"Cannot add more than {max_tasks} tasks to a project.")
        task.container_project = self
        self.project_tasks.append(task)

    def show_tasks(self) -> None:
        """
        Display all tasks associated with the project.
        return: None
        """

        # Check if there are any tasks
        if len(self.project_tasks) == 0:
            print(f"No tasks in Project '{self.project_name}'.")
            return
        # List each task with its details
        result_string = f"Tasks in Project '{self.project_name}':\n"
        for task in self.project_tasks:
            result_string += (f"{task.task_id} - {task.task_name} - {task.task_description} | "
                              f"Status: {task.task_status} | Due: {task.task_due_date}\n")
        print(result_string)

    def __str__(self):
        return f"Project: {self.project_name} - {self.project_description}"

    def __repr__(self):
        return self.__str__()

