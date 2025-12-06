# ToDo List Project - Phase 3 (Web API)

A Python-based ToDo List application with a RESTful Web API built using FastAPI. The application uses SQLAlchemy ORM with a clean layered architecture (models, repositories, services). Configuration is driven via a `.env` file and dependencies are managed by Poetry (`pyproject.toml`).

## Phase 3: Migration to Web API

** IMPORTANT: The CLI interface has been deprecated and will be removed in Phase 4.**

This version introduces a modern RESTful API using FastAPI, replacing the command-line interface. All features previously available through CLI are now accessible via HTTP endpoints.

## Features

### API Features (Phase 3)
- **RESTful API** with FastAPI
- **Automatic API Documentation** (Swagger UI & ReDoc)
- **Request/Response Validation** with Pydantic
- **Async Support** for high performance
- **OpenAPI 3.0 Specification**
- **CORS Support** for web clients
- **Comprehensive Error Handling**

### Application Features
- **Project Management**:
  - Create, read, update, delete projects
  - Unique project names enforced
  - List all projects
- **Task Management**:
  - Create, read, update, delete tasks
  - Unique task names per project
  - Task status management (TODO, DOING, DONE)
  - Due date and closed_at tracking
- **Cascade Operations**: Deleting a project removes all its tasks
- **Clean Architecture**: Controller → Service → Repository layers


## Setup

### 1. Install Dependencies

```bash
# Ensure Python 3.11+ and Poetry are installed
poetry install
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./todo.db
MAX_SHOW_NAME_LENGTH=10
MAX_SHOW_DESCRIPTION_LENGTH=15
MAX_SHOW_DUE_DATE_LENGTH=10
MAX_SHOW_CLOSED_AT_LENGTH=10
```

### 3. Initialize Database

```bash
# Run migrations
alembic upgrade head
```

## How to use

### Start the API Server

```bash
# Using uvicorn directly
poetry run uvicorn app.api_main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
poetry run python -m app.api_main
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/api/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

All documents of how to use the API are automatically generated and available at the above URLs.
### Example API Usage

```bash
# Create a project
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "description": "Work tasks"}'

# List all projects
curl "http://localhost:8000/api/v1/projects"

# Create a task
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Complete report",
    "description": "Finish quarterly report",
    "status": "todo",
    "project_id": 1
  }'
```

## Project Structure

```
clonetodo/
├─ app/
│  ├─ api/
│  │  └─ v1/
│  │     ├─ controllers/
│  │     │  ├─ projects.py      # Project endpoints
│  │     │  └─ tasks.py         # Task endpoints
│  │     ├─ schemas/
│  │     │  ├─ requests/
│  │     │  │  ├─ project.py    # Request models for projects
│  │     │  │  └─ task.py       # Request models for tasks
│  │     │  └─ responses/
│  │     │     ├─ project.py    # Response models for projects
│  │     │     └─ task.py       # Response models for tasks
│  │     ├─ dependencies/
│  │     │  └─ services.py      # Dependency injection
│  │     └─ routers.py          # API router configuration
│  ├─ cli/                       # ⚠️ DEPRECATED
│  │  └─ console.py             # CLI interface (deprecated)
│  ├─ db/
│  │  ├─ base.py                # SQLAlchemy Base
│  │  └─ session.py             # Database session management
│  ├─ models/
│  │  ├─ project.py             # Project ORM model
│  │  └─ task.py                # Task ORM model
│  ├─ repositories/
│  │  ├─ project_repository.py  # Project data access
│  │  └─ task_repository.py     # Task data access
│  ├─ services/
│  │  ├─ project_services.py    # Project business logic
│  │  └─ task_services.py       # Task business logic
│  ├─ exceptions/
│  │  └─ service_exceptions.py  # Custom exceptions
│  ├─ api_main.py               # FastAPI application
│  └─ main.py                   # Legacy main file
├─ alembic/                     # Database migrations
├─ .env                         # Environment configuration
├─ pyproject.toml               # Poetry dependencies
└─ README.md                    # This file
```

## ⚠️ CLI Deprecation Notice

The CLI interface (`app.cli.console`) is **deprecated** as of Phase 3 and will be **removed in Phase 4**.

### Migration Guide

All CLI functionality is available through the API:

| CLI Command | API Endpoint |
|------------|--------------|
| `project create` | `POST /api/v1/projects` |
| `project list` | `GET /api/v1/projects` |
| `project find` | `GET /api/v1/projects/{id}` |
| `project delete` | `DELETE /api/v1/projects/{id}` |
| `project set_name` | `PUT /api/v1/projects/{id}` |
| `task create` | `POST /api/v1/tasks` |
| `task list` | `GET /api/v1/tasks` |
| `task find` | `GET /api/v1/tasks/{id}` |
| `task delete` | `DELETE /api/v1/tasks/{id}` |

**Why migrate to the API?**
- Better scalability and performance
- Standardized RESTful interface
- Automatic documentation
- Easy integration with web/mobile apps
- Supports modern microservices architecture

## Documentation

- **Interactive API Docs**: Visit http://localhost:8000/api/docs after starting the server
- **API Reference**: Available at http://localhost:8000/api/redoc
- All endpoints include detailed descriptions, request/response schemas, and examples


## Version History

- **v3.0.0** (Phase 3): FastAPI Web API implementation, CLI deprecated
- **v2.0.0** (Phase 2): SQLAlchemy ORM integration, CLI enhancements
- **v1.0.0** (Phase 1): Initial In-Memory ToDo List application