# ToDo List Project

A Python-based ToDo List application using SQLAlchemy ORM with a clean layered architecture (models, repositories, services). It supports creating projects and tasks, updating their fields, and printing formatted tables to the console. Configuration is driven via a `.env` file and dependencies are managed by Poetry (`pyproject.toml`).

## Features

- User-like workflow via services
- Project Management:
  - Create, read, update (name/description), delete
  - Unique project names enforced
  - List all projects, print tables
- Task Management:
  - Create, read, update (name/description/status/due_date/closed_at/project_id), delete
  - Unique task names per project enforced
  - List all tasks, print tables
- Cascade-like behavior handled in service layer (delete project -> delete its tasks)
- Environment-based output width controls for CLI printing

## Tech Stack

- Python 3.x
- SQLAlchemy (ORM)
- Poetry with `pyproject.toml`
- python-dotenv for configuration

## Setup

1. Ensure Python and Poetry are installed.
2. In the project root, configure environment variables in `.env`:
   - DATABASE_URL: SQLAlchemy URL (e.g. `sqlite:///./todo.db`)
   - MAX_SHOW_NAME_LENGTH (default: 10)
   - MAX_SHOW_DESCRIPTION_LENGTH (default: 15)
   - MAX_SHOW_DUE_DATE_LENGTH (default: 10)
   - MAX_SHOW_CLOSED_AT_LENGTH (default: 10)
3. Install dependencies with Poetry:
   - `poetry install`
4. Initialize the database tables where you bootstrap the app (ensure you run `alembic upgrade head` if using Alembic for migrations).

## Using console.py

Example of usage via `console.py`:

- Create a project:
  - `python -m app.cli.console project create --name = "Work" --description = "Work tasks"`
- List projects:
  - `python -m app.cli.console project list`

## Project Structure

```
Project-2-ToDo-List/
├─ app/
│  ├─ db/
│  │  ├─ base.py              # SQLAlchemy Base (metadata) definition
│  │  └─ session.py           # Engine + SessionLocal via DATABASE_URL (.env)
│  ├─ models/
│  │  ├─ project.py           # Project model (name, description, tasks)
│  │  └─ task.py              # Task model (name, description, status, dates, FK)
│  ├─ repositories/
│  │  ├─ project_repository.py# CRUD for Project + list tasks
│  │  └─ task_repository.py   # CRUD for Task
│  ├─ services/
│  │  ├─ project_services.py  # Business rules + printing + cascade delete
│  │  └─ task_services.py     # Business rules + printing + validations
│  ├─ exceptions/
│  │  └─ service_exceptions.py# Domain-specific errors
│  └─ main.py                 # Wires Session, repositories, and services
├─ .env                       # Configuration (DATABASE_URL, print widths)
├─ README.md                  # This file
└─ pyproject.toml             # Poetry configuration and deps
```
