from User import User

from Project import Project

from Task import Task

if __name__ == "__main__":
    me = User(username="Nima")
    project = Project(project_name="TestProject1")
    project2 = Project(project_name="TestProject2")
    me.add_project(project)
    me.add_project(project2)
    project.add_task(Task(task_name="Task1", task_description="This is task 1"))
    project.add_task(Task(task_name="Task2", task_description="This is task 2"))
    project2.add_task(Task(task_name="Task3", task_description="This is task 3"))

    print(me)
    me.show_projects()
    me.show_tasks()