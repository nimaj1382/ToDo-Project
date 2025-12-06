from fastapi import APIRouter

from app.api.v1.controllers import projects, tasks

# Create main API v1 router
api_router = APIRouter()

# Include all controller routers
api_router.include_router(
    projects.router,
    tags = ["projects"]
)

api_router.include_router(
    tasks.router,
    tags = ["tasks"]
)