from typing import Optional, List

from sqlalchemy.orm import Session
from app.models.project import Project


class ProjectRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.session.query(Project).filter(Project.id == project_id).first()

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        return self.session.query(Project).filter(Project.name == project_name).first()

    def add_project(self, project: Project) -> None:
        self.session.add(project)
        self.session.commit()

    def delete_project(self, project: Project) -> None:
        self.session.delete(project)
        self.session.commit()

    def set_project_name(self, project: Project, new_project_name: str) -> None:
        project.name = new_project_name
        self.session.commit()

    def set_project_description(self, project: Project, new_project_description: str) -> None:
        project.description = new_project_description
        self.session.commit()

    def project_tasks_list(self, project: Project) -> List["Task"]:
        return list(project.tasks)