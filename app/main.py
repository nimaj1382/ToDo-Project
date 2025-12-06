from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import *
from app.repositories import *
from app.services import *
from datetime import datetime

db = SessionLocal()

project_repo = ProjectRepository(db)
task_repo = TaskRepository(db)
project_service = ProjectService(project_repo)
task_service = TaskService(task_repo)

