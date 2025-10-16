import os

from datetime import datetime

from dotenv import load_dotenv

from Exceptions import MaxLimitExceededError

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
        raise ValueError: If the project is not a Project instance.
        raise MaxLimitExceededError: If adding the project exceeds the maximum limit.
        raise ValueError: If the project name is not unique within the user's projects.
        """

        # Check if the project is a Project instance
        if not isinstance(project, Project):
            raise ValueError("Only Project instances can be added.")
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


class Task:

    _task_ids_set = set()
    _task_id_counter = 1

    def __init__(self, *, task_name: str = None, task_description: str = None,
                 task_status: str = "todo", task_due_date: str = None):
        """
        Initialize a Task instance with optional name, description, status, and due date.
        param task_name: Optional name for the task.
        param task_description: Optional description for the task.
        param task_status: Optional status for the task. Must be
            one of "todo", "doing", or "done". Default is "todo".
        param task_due_date: Optional due date for the task in 'YYYY-MM-DD' format.
        return: None
        raise ValueError: If task_status is not one of the allowed values.
        raise ValueError: If task_due_date is not in 'YYYY-MM-DD' format.
        """

        self._task_name = None
        self._task_description = None
        self._task_status = "todo"
        self._task_due_date = None
        self.container_project = None
        self._task_id = Task._task_id_counter
        self.__class__._task_ids_set.add(self._task_id)
        self.__class__._task_id_counter += 1

        if task_name:
            self.task_name = task_name
        if task_description:
            self.task_description = task_description
        if task_status:
            self.task_status = task_status
        if task_due_date:
            self.task_due_date = task_due_date

    @property
    def task_name(self):
        return self._task_name

    @task_name.setter
    def task_name(self, value: str) -> None:
        # Ensure task name length does not exceed the limit
        if len(value) <= 30:
            self._task_name = value
        else:
            raise ValueError("Task name must be 30 characters or fewer.")

    @property
    def task_description(self):
        return self._task_description

    @task_description.setter
    def task_description(self, value: str) -> None:
        # Ensure task description length does not exceed the limit
        if len(value) <= 150:
            self._task_description = value
        else:
            raise ValueError("Task description must be 150 characters or fewer.")

    @property
    def task_status(self):
        return self._task_status

    @task_status.setter
    def task_status(self, value: str) -> None:
        # Ensure task status is one of the allowed values
        if value in ["todo", "doing", "done"]:
            self._task_status = value
        else:
            raise ValueError("Task status must be \"todo\", \"doing\", or \"done\".")

    @property
    def task_due_date(self):
        return self._task_due_date

    @task_due_date.setter
    def task_due_date(self, value: str) -> None:
        """
        Set the due date for the task.
        param value: Due date string in 'YYYY-MM-DD' format.
        return: None
        raise ValueError: If the date is not in 'YYYY-MM-DD' format.
        """
        # Ensure task due date is in 'YYYY-MM-DD' format
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self._task_due_date = value
        except ValueError:
            raise ValueError("Task due date must be in 'YYYY-MM-DD' format.")

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value: int) -> None:
        raise AttributeError("Task ID is read-only and cannot be modified.")

    def set_name(self, new_name: str) -> None:
        self.task_name = new_name

    def set_description(self, new_description: str) -> None:
        self.task_description = new_description

    def set_status(self, new_status: str) -> None:
        """
        Change the status of the task. Must be one of \"todo\", \"doing\", or \"done\".
        param new_status: New status string for the task.
        return: None
        raise ValueError: If new_status is not one of the allowed values.
        """

        self.task_status = new_status

    def set_due_date(self, new_due_date: str) -> None:
        self.task_due_date = new_due_date

    def delete_task(self) -> None:
        # Remove the task from its container project's task list
        if self.container_project and self in self.container_project.project_tasks:
            self.container_project.project_tasks.remove(self)
        # Remove the task ID from the class-level set
        if self.__class__._task_ids_set:
            self.__class__._task_ids_set.remove(self.task_id)
        del self

    def __str__(self) -> str:
        return (f"Task: {self.task_name} - {self.task_description} | Status: {self.task_status} "
                f"| Due: {self.task_due_date}")

    def __repr__(self) -> str:
        return self.__str__()