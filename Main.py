from Classes import *

if __name__ == "__main__":
    new_project = Project("My Project", "This is a new project.")

    second_project = Project("My Project 2", "This is another project.")

    new_project.add_task(Task(task_name="first task"))
    print(new_project.project_tasks)

    print(new_project)
    print(second_project)
