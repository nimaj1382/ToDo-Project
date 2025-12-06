from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Project(Base):
    """SQLAlchemy model representing a project.

    Attributes:
        id (int): Primary key identifier.
        name (str): Unique project name, max length 30.
        description (str): Optional project description, max length 150.
        tasks (list[Task]): Relationship to associated Task models.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False, index=True)
    description = Column(String(150), index=True)
    # Bidirectional relationship with Task; Task.project refers back here
    tasks = relationship("Task", back_populates="project")