from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.db.base import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind = engine)

# Create FastAPI application
app = FastAPI(
    title = "ToDo List API",
    description = """
    A RESTful API for managing projects and tasks.

    ## Features

    * **Projects**: Create, read, update, and delete projects
    * **Tasks**: Create, read, update, and delete tasks within projects
    * **Validation**: Automatic request/response validation with Pydantic
    * **Documentation**: Interactive API documentation with Swagger UI

    ## Migration from CLI

    This API replaces the deprecated CLI interface. All functionality previously 
    available via CLI is now accessible through these REST endpoints.
    """,
    version = "3.0.0",
    docs_url = "/api/docs",
    redoc_url = "/api/redoc",
    openapi_url = "/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # In production, specify allowed origins
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Include API v1 router
app.include_router(
    api_router,
    prefix = "/api/v1",
)


@app.get("/", tags = ["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ToDo List API",
        "version": "3.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }


@app.get("/health", tags = ["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host = "0.0.0.0", port = 8000)