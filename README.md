# ToDo List Project

A simple Python-based ToDo List application that allows users create and manage projects and tasks. The application supports user management, project management, and task management with configurable limits.

## Features

- **User Management:** Create users with a username and full name.
- **Project Management:** Add, view, and delete projects for each user.
- **Task Management:** Add, view, update, and delete tasks within projects.

## Usage

1. Clone the repository or copy the files to your local machine.
2. Use Poetry to manage dependencies using the provided `pyproject.toml` file.
3. Create a `.env` file to configure project and task limits
4. Run the `main.py` file to see example usage.

## File Structure

- `main.py` - Example usage and entry point.
- `user.py` - User class.
- `project.py` - Project class.
- `task.py` - Task class.
- `exceptions.py` - Custom exception definitions.
- `.env` - Configuration for project/task limits.

## Example

See `main.py` for example usage of the classes and methods.