import threading
import time
from typing import Callable, Optional

from autoclose_overdue import autoclose_overdue_tasks

class Scheduler:
    """
    Periodically runs a given function in a background thread.

    Notes:
        - Uses a daemon thread so it won't block interpreter shutdown.
        - A threading.Event is used to signal termination cleanly.
    """

    def __init__(self, interval: int,
                 task: Callable,
                 args: Optional[tuple] = None,
                 kwargs: Optional[dict] = None) -> None:
        """
        Args:
            interval (int): Interval in seconds between task executions.
            task (Callable): The function to run periodically.
            args (tuple, optional): Positional arguments for the task.
            kwargs (dict, optional): Keyword arguments for the task.
        """
        self.interval = interval
        self.task = task
        self.args = args if args else ()
        self.kwargs = kwargs if kwargs else {}
        self._stop_event = threading.Event()
        # Daemon thread so the program can exit without waiting for this thread.
        self._thread = threading.Thread(target = self._run, daemon = True)

    def _run(self) -> None:
        """Worker loop that executes the task, then sleeps for the interval."""
        while not self._stop_event.is_set():
            # Execute the provided callable with any given args/kwargs.
            self.task(*self.args, **self.kwargs)
            time.sleep(self.interval)

    def start(self) -> None:
        """
        Start the scheduler in a background thread.
        """
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the scheduler.
        """
        self._stop_event.set()
        self._thread.join()

# WARNING: Creating and starting a scheduler at import-time introduces a side effect.
# Importing this module will immediately start the background task runner.
scheduler = Scheduler(interval = 3600, task = autoclose_overdue_tasks)  # Run every hour
scheduler.start()