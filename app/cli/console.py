"""
Command-line interface (CLI) for the ToDo List application.

This module defines the CLI using argparse, providing subcommands for
project and task operations, plus a top-level command to list all projects
with their tasks. It wires repositories and services, parses user input,
and routes each command to the corresponding service methods.

Key concepts:
- Top-level entities: "project", "task", and "list_all".
- Each entity has subcommands implemented via argparse subparsers.
- Mutually exclusive groups enforce that only one of --id or --name is
  provided where applicable.
- Date strings from CLI are parsed to datetime objects when necessary.
"""
import argparse
from datetime import datetime
from app.commands.autoclose_overdue import autoclose_overdue_tasks
from app.services import *
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

session = SessionLocal()
project_repo = ProjectRepository(session)
task_repo = TaskRepository(session)
project_service = ProjectService(project_repo)
task_service = TaskService(task_repo)

def main():
    parser = argparse.ArgumentParser(description = "ToDo List CLI")
    subparsers = parser.add_subparsers(dest = "entity", required = True)

    # Project commands
    project_parser = subparsers.add_parser("project", help = "Project operations")
    project_subparsers = project_parser.add_subparsers(dest = "action", required = True)

    # project create
    project_create = project_subparsers.add_parser("create", help = "Create a new project")
    project_create.add_argument("--name", required = True, help = "Project name")
    project_create.add_argument("--description", default = "",
                                help = "Project description")

    # project list
    project_list = project_subparsers.add_parser("list", help = "List all projects")

    # project delete (by id or name)
    project_delete = project_subparsers.add_parser("delete",
                                help = "Delete a project by id or name")
    # Using a mutually exclusive group forces the user to choose either --id or --name,
    # preventing ambiguous inputs and simplifying downstream logic.
    project_delete_group = project_delete.add_mutually_exclusive_group(required = True)
    project_delete_group.add_argument("--id", type = int, help = "Project id")
    project_delete_group.add_argument("--name", type = str, help = "Project name")

    # project set name
    project_set_name = project_subparsers.add_parser("set_name",
                                help = "Set a new name for a project by id or name")
    project_set_name_group = project_set_name.add_mutually_exclusive_group(required = True)
    project_set_name_group.add_argument("--id", type = int, help = "Project id")
    project_set_name_group.add_argument("--name", type = str, help = "Project name")
    project_set_name.add_argument("--new_name", required = True, 
                                  help = "New project name")

    # project set description
    project_set_desc = project_subparsers.add_parser("set_description",
                                help = "Set a new description for a project by id or name")
    project_set_desc_group = project_set_desc.add_mutually_exclusive_group(required = True)
    project_set_desc_group.add_argument("--id", type = int, help = "Project id")
    project_set_desc_group.add_argument("--name", type = str, help = "Project name")
    project_set_desc.add_argument("--new_description",
                                required = True, help = "New project description")

    # project find
    project_find = project_subparsers.add_parser("find", 
                                help = "Find a project by id or name")
    project_find_group = project_find.add_mutually_exclusive_group(required = True)
    project_find_group.add_argument("--id", type = int, help = "Project id")
    project_find_group.add_argument("--name", type = str, help = "Project name")

    # project list_tasks
    project_list_tasks = project_subparsers.add_parser("list_tasks",
                                help = "List all tasks for a project by id or name")
    project_list_tasks_group = project_list_tasks.add_mutually_exclusive_group(required = True)
    project_list_tasks_group.add_argument("--id", type = int, help = "Project id")
    project_list_tasks_group.add_argument("--name", type = str, help = "Project name")

    # Task commands
    task_parser = subparsers.add_parser("task", help = "Task operations")
    task_subparsers = task_parser.add_subparsers(dest = "action", required = True)

    # task create
    task_create = task_subparsers.add_parser("create", help = "Create a new task")
    task_create.add_argument("--project_id", type = int, required = True,
                             help = "Project ID for the task")
    task_create.add_argument("--name", required = True, help = "Task name")
    task_create.add_argument("--description", default = "", help = "Task description")
    task_create.add_argument("--due_date", default = None,
                             help = "Task due date (YYYY-MM-DD)")

    # task list
    task_list = task_subparsers.add_parser("list", help = "List all tasks")

    # task delete (by id)
    task_delete = task_subparsers.add_parser("delete", help = "Delete a task by id")
    task_delete.add_argument("--id", type = int, required = True, help = "Task id")

    # task set name
    task_set_name = task_subparsers.add_parser("set_name",
                            help = "Set a new name for a task by id")
    task_set_name.add_argument("--id", type = int, required = True, help = "Task id")
    task_set_name.add_argument("--new_name", required = True, help = "New task name")

    # task set description
    task_set_desc = task_subparsers.add_parser("set_description",
                            help = "Set a new description for a task by id")
    task_set_desc.add_argument("--id", type = int, required = True, help = "Task id")
    task_set_desc.add_argument("--new_description", required = True,
                            help = "New task description")

    # task set due date
    task_set_due_date = task_subparsers.add_parser("set_due_date",
                            help = "Set a new due date for a task by id")
    task_set_due_date.add_argument("--id", type = int, required = True, 
                                   help = "Task id")
    task_set_due_date.add_argument("--due_date", required = True,
                            help = "New due date (YYYY-MM-DD)")

    # task set status
    task_set_status = task_subparsers.add_parser("set_status",
                            help = "Set a new status for a task by id")
    task_set_status.add_argument("--id", type = int, required = True, help = "Task id")
    task_set_status.add_argument("--status", required = True,
                            choices = ["todo", "doing", "done"], help = "New task status")

    # task find
    task_find = task_subparsers.add_parser("find", help = "Find a task by id or name")
    task_find_group = task_find.add_mutually_exclusive_group(required = True)
    task_find_group.add_argument("--id", type = int, help = "Task id")
    task_find_group.add_argument("--name", type = str, help = "Task name")

    # task set project id
    task_set_project_id = task_subparsers.add_parser("set_project_id",
                            help = "Set a new project id for a task by id")
    task_set_project_id.add_argument("--id", type = int, required = True, 
                                     help = "Task id")
    task_set_project_id.add_argument("--project_id", type = int, required = True,
                            help = "New project id for the task")

    # task set closed_at
    task_set_closed_at = task_subparsers.add_parser("set_closed_at",
                            help = "Set closed_at datetime for a task by id")
    task_set_closed_at.add_argument("--id", type = int, required = True, 
                                    help = "Task id")
    # Note: help suggests time component, but parsing below uses YYYY-MM-DD.
    # Keeping as-is to avoid logic changes; parsing comment clarifies behavior.
    task_set_closed_at.add_argument("--closed_at", required = True,
                            help = "Closed at datetime (YYYY-MM-DD HH:MM:SS)")

    # Add a top-level command for listing all projects with their tasks
    list_all_parser = subparsers.add_parser("list_all",
                            help = "List all projects and their tasks")

    args = parser.parse_args()

    # Routing: based on top-level entity, delegate to appropriate service methods.
    if args.entity == "list_all":
        # This uses project_service with task_service to print a combined view
        # of all projects and their tasks.
        project_service.print_all_projects_with_tasks(task_service)
        return
    if args.entity == "project":
        if args.action == "create":
            try:
                project_service.create_project(project_name = args.name,
                                               project_description = args.description)
                print("Project created successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "list":
            project_service.print_all_projects()
        elif args.action == "delete":
            # Defensive check: although argparse enforces mutual exclusivity,
            # this ensures no ambiguity if both were somehow provided.
            if args.id is not None and args.name is not None:
                print("Error: Only one of --id or --name should be provided.")
                return
            try:
                if args.id is not None:
                    project_service.delete_project_by_id(args.id, task_service)
                elif args.name is not None:
                    project_service.delete_project_by_name(args.name, task_service)
                print("Project deleted successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_name":
            if args.id is not None and args.name is not None:
                print("Error: Only one of --id or --name should be provided.")
                return
            try:
                if args.id is not None:
                    project_service.set_project_name_by_id(args.id, args.new_name)
                elif args.name is not None:
                    project_service.set_project_name_by_name(args.name, args.new_name)
                print("Project name updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_description":
            if args.id is not None and args.name is not None:
                print("Error: Only one of --id or --name should be provided.")
                return
            try:
                if args.id is not None:
                    project_service.set_project_description_by_id(args.id, args.new_description)
                elif args.name is not None:
                    project_service.set_project_description_by_name(args.name, args.new_description)
                print("Project description updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "find":
            if args.id is not None and args.name is not None:
                print("Error: Only one of --id or --name should be provided.")
                return
            try:
                project = None
                if args.id is not None:
                    project = project_service.get_project_by_id(args.id)
                elif args.name is not None:
                    project = project_service.get_project_by_name(args.name)
                if project:
                    project_service.print_project(project)
                else:
                    print("Project not found.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "list_tasks":
            if args.id is not None and args.name is not None:
                print("Error: Only one of --id or --name should be provided.")
                return
            try:
                tasks = []
                if args.id is not None:
                    tasks = project_service.project_tasks_list_by_id(args.id)
                elif args.name is not None:
                    tasks = project_service.project_tasks_list_by_name(args.name)
                if not tasks:
                    print("No tasks found for the specified project.")
                    return
                for task in tasks:
                    task_service.print_task(task)
            except Exception as e:
                print(f"Error: {e}")
    elif args.entity == "task":
        if args.action == "create":
            due_date = None
            if args.due_date:
                try:
                    # Parse YYYY-MM-DD into a datetime; if invalid, skip gracefully.
                    due_date = datetime.strptime(args.due_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Skipping due date.")
            try:
                task_service.create_task(task_name = args.name,
                                         task_description = args.description,
                                         task_project_id = args.project_id,
                                         task_due_date = due_date,
                                         project_service = project_service)
                print("Task created successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "list":
            task_service.print_all_tasks()
        elif args.action == "delete":
            try:
                task_service.delete_task_by_id(args.id)
                print("Task deleted successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_name":
            try:
                task_service.set_task_name_by_id(args.id, args.new_name)
                print("Task name updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_description":
            try:
                task_service.set_task_description_by_id(args.id, args.new_description)
                print("Task description updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_due_date":
            try:
                due_date = None
                if args.due_date:
                    from datetime import datetime
                    due_date = datetime.strptime(args.due_date, "%Y-%m-%d")
                task_service.set_task_due_date_by_id(args.id, due_date)
                print("Task due date updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_status":
            try:
                from app.models.task import TaskStatus
                status = TaskStatus(args.status)
                task_service.set_task_status_by_id(args.id, status)
                print("Task status updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_project_id":
            try:
                task_service.set_task_project_id_by_id(args.id, args.project_id, project_service)
                print("Task project id updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "find":
            if args.id is not None and args.name is not None:
                print("Error: Only one of --id or --name should be provided.")
                return
            try:
                task = None
                if args.id is not None:
                    task = task_service.get_task_by_id(args.id)
                elif args.name is not None:
                    tasks = task_service.get_tasks_by_name(args.name)
                    if not tasks:
                        print("Task not found.")
                        return
                    for task in tasks:
                        task_service.print_task(task)
                    return
                if task:
                    task_service.print_task(task)
                else:
                    print("Task not found.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "set_closed_at":
            try:
                closed_at = None
                if args.closed_at:
                    from datetime import datetime
                    # Despite help suggesting a datetime with time, this parses
                    # only date (YYYY-MM-DD). Keeping to match current behavior.
                    closed_at = datetime.strptime(args.closed_at, "%Y-%m-%d")
                task_service.set_task_closed_at_by_id(args.id, closed_at)
                print("Task closed_at updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
        elif args.action == "autoclose_overdue":
            try:
                autoclose_overdue_tasks()
                print("Overdue tasks closed successfully.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()




