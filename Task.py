from datetime import datetime

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