from dotenv import load_dotenv
import os
from datetime import datetime


class User:

    def __init__(self, *, username: str = None, full_name: str = None):
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
        if not isinstance(project, Project):
            raise ValueError("Only Project instances can be added.")
        load_dotenv()
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 30))
        if len(self.projects) >= max_projects:
            raise Exception(f"Cannot add more than {max_projects} projects to a user.")
        for p in self.projects:
            if p.project_name == project.project_name:
                raise ValueError("Project name must be unique within the user's projects.")
        self.projects.append(project)

    def show_projects(self) -> None:
        result_string = f"{self.username}'s Projects:\n"
        for project in self.projects:
            result_string += f"{project.project_name} - {project.project_description}\n"
        print(result_string)

    def remove_user(self) -> None:
        for project in self.projects:
            project.delete_project()
        del self

    def __str__(self) -> str:
        return f"User: {self.username} - {self.full_name}"

    def __repr__(self) -> str:
        return self.__str__()



class Project:

    __total_project_number = 0
    __project_names_set = set()

    def __init__(self, project_name: str = None, project_description: str = None):
        load_dotenv()
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 30))
        if self.__class__.__total_project_number + 1 > max_projects:
            raise Exception(f"Cannot create more than {max_projects} projects.")

        self._project_name = None
        self._project_description = None
        self._project_tasks = []

        if project_name:
            self.project_name = project_name
        if project_description:
            self.project_description = project_description

        self.__class__.__total_project_number += 1

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value: str) -> None:
        if value in self.__class__.__project_names_set:
            raise ValueError("Project name must be unique.")
        else:
            self.__class__.__project_names_set.add(value)
            if self._project_name is not None:
                self.__class__.__project_names_set.remove(self._project_name)

        if len(value) <= 30:
            self._project_name = value
        else:
            raise ValueError("Project name must be 30 characters or fewer.")

    @property
    def project_description(self):
        return self._project_description

    @project_description.setter
    def project_description(self, value: str) -> None:
        if len(value) <= 150:
            self._project_description = value
        else:
            raise ValueError("Project description must be 100 characters or fewer.")

    @property
    def project_tasks(self):
        return self._project_tasks


    def set_name(self, new_name: str) -> None:
        if self.project_name in self.__class__.__project_names_set:
            self.__class__.__project_names_set.remove(self.project_name)

        if new_name in self.__class__.__project_names_set:
            raise ValueError("Project name must be unique.")
        else:
            self.project_name = new_name
            self.__class__.__project_names_set.add(self.project_name)

    def set_description(self, new_description: str) -> None:
        self.project_description = new_description

    def delete_project(self):
        if self.project_name in self.__class__.__project_names_set:
            self.__class__.__project_names_set.remove(self.project_name)

        self.__class__.__total_project_number -= 1
        del self

    def add_task(self, task: "Task") -> None:
        """
        Add a Task instance to the project's task list.
        param task: Task instance to be added.
        return: None
        """

        if not isinstance(task, Task):
            raise ValueError("Only Task instances can be added.")
        load_dotenv()
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASKS", 20))
        if len(self.project_tasks) >= max_tasks:
            raise Exception(f"Cannot add more than {max_tasks} tasks to a project.")
        task.container_project = self
        self.project_tasks.append(task)

    def __str__(self):
        return f"Project: {self.project_name} - {self.project_description}"

    def __repr__(self):
        return self.__str__()


class Task:

    def __init__(self, *, task_name: str = None, task_description: str = None, task_status: str = "todo", task_due_date: str = None):
        self._task_name = None
        self._task_description = None
        self._task_status = "todo"
        self._task_due_date = None
        self.container_project = None

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
        if len(value) <= 30:
            self._task_name = value
        else:
            raise ValueError("Task name must be 30 characters or fewer.")

    @property
    def task_description(self):
        return self._task_description

    @task_description.setter
    def task_description(self, value: str) -> None:
        if len(value) <= 150:
            self._task_description = value
        else:
            raise ValueError("Task description must be 150 characters or fewer.")

    @property
    def task_status(self):
        return self._task_status

    @task_status.setter
    def task_status(self, value: str) -> None:
        if value in ["todo", "doing", "done"]:
            self._task_status = value
        else:
            raise ValueError("Task status must be \"todo\", \"doing\", or \"done\".")

    @property
    def task_due_date(self):
        return self._task_due_date

    @task_due_date.setter
    def task_due_date(self, value: str) -> None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self._task_due_date = value
        except ValueError:
            raise ValueError("Task due date must be in 'YYYY-MM-DD' format.")

    def set_name(self, new_name: str) -> None:
        self.task_name = new_name

    def set_description(self, new_description: str) -> None:
        self.task_description = new_description

    def set_status(self, new_status: str) -> None:
        """
        Change the status of the task. Must be one of \"todo\", \"doing\", or \"done\".
        param new_status: New status string for the task.
        return: None
        """
        self.task_status = new_status

    def set_due_date(self, new_due_date: str) -> None:
        self.task_due_date = new_due_date

    def delete_task(self) -> None:
        if self.container_project and self in self.container_project.project_tasks:
            self.container_project.project_tasks.remove(self)
        del self

    def __str__(self) -> str:
        return f"Task: {self.task_name} - {self.task_description} | Status: {self.task_status} | Due: {self.task_due_date}"

    def __repr__(self) -> str:
        return self.__str__()