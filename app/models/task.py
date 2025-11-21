from sqlalchemy import (Column, Integer, String, ForeignKey, Enum,
                        DateTime, UniqueConstraint)
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False, index=True)
    description = Column(String(150))
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    due_date = Column(DateTime)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"),
                        nullable=False)
    project = relationship("Project", back_populates="tasks")

    __table_args__ = (
        UniqueConstraint('project_id', 'title', name='uq_project_task_name'),
    )