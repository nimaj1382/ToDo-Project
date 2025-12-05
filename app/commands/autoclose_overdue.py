import schedule
import time
from datetime import datetime
from app.models.task import TaskStatus

def autoclose_overdue_tasks(task_service: 'TaskService' = None):
    tasks = task_service.all_tasks()
    now = datetime.now()
    for task in tasks:
        if task.due_date and task.due_date < now and task.status != TaskStatus.DONE:
            task_service.set_task_status(task, TaskStatus.DONE)
            task_service.set_task_closed_at(task, now)

# Schedule the autoclose function to run every 2 hours
schedule.every(2).hours.do(autoclose_overdue_tasks)