from sqlalchemy import (Column, Integer, String, ForeignKey, Enum,
                        DateTime, UniqueConstraint)
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class TaskStatus(enum.Enum):
    """Enumeration of possible task statuses."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

    def __str__(self):
        """Return the lowercase string value of the status.

        This is useful for printing and for CLI outputs.
        """
        if self == self.TODO:
            return "todo"
        if self == self.DOING:
            return "doing"
        if self == self.DONE:
            return "done"

class Task(Base):
    """SQLAlchemy model representing a task.

    Attributes:
        id (int): Primary key identifier.
        name (str): Task name, max length 30.
        description (str): Optional task description, max length 150.
        status (TaskStatus): Current status, defaults to TODO.
        due_date (datetime): Optional due date.
        closed_at (datetime): Optional timestamp when the task was completed/closed.
        project_id (int): Foreign key reference to the owning project.
        project (Project): Relationship to the parent Project model.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(30), nullable = False, index = True)
    description = Column(String(150))
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable = False)
    due_date = Column(DateTime)
    closed_at = Column(DateTime)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete = "CASCADE"),
                        nullable=False)
    project = relationship("Project", back_populates = "tasks")
    # Ensure task names are unique within the same project scope
    __table_args__ = (
        UniqueConstraint('project_id', 'name', name = 'uq_project_task_name'),
    )