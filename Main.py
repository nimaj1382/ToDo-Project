from Classes import *

if __name__ == "__main__":
    me = User(username="Nima")
    me.add_project(Project(project_name="TestProject"))

    me.show_projects()
    print(me)
