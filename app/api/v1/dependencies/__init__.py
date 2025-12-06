"""API v1 dependencies.

FastAPI dependencies used by controllers (e.g., service providers).
"""
from .services import get_db, get_project_service, get_task_service

__all__ = [
    "get_db",
    "get_project_service",
    "get_task_service",
]