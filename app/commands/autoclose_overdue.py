import schedule
import time
from datetime import datetime
from app.models.task import TaskStatus

"""Utilities for automatically closing overdue tasks.

This module defines a function to scan all tasks and close those past their due date.
It also sets up a periodic schedule at import time.

Note: Scheduling at import time introduces side effects and may not be desired in
all execution contexts (e.g., unit tests). Import cautiously.
"""

def autoclose_overdue_tasks(task_service: 'TaskService' = None):
    """Set tasks to DONE when overdue and stamp their closed_at.

    Iterates over all tasks and, for any task with a due_date in the past and a
    non-DONE status, marks it DONE and sets closed_at to now.

    Args:
        task_service (TaskService, optional): Service used to access and update tasks.
            Expected to be provided by the application wiring/DI layer.
    """
    tasks = task_service.all_tasks()
    now = datetime.now()
    for task in tasks:
        # Only close tasks that are overdue and not already completed.
        if task.due_date and task.due_date < now and task.status != TaskStatus.DONE:
            task_service.set_task_status(task, TaskStatus.DONE)
            task_service.set_task_closed_at(task, now)

# Schedule the autoclose function to run every 2 hours
# Caution: This runs at import time and may create background jobs unintentionally.
schedule.every(2).hours.do(autoclose_overdue_tasks)