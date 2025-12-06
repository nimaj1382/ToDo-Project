from typing import Optional, List, Type

from sqlalchemy.orm import Session

from app.models.project import Project

class ProjectRepository:
    """Repository encapsulating database operations for Project.

    Attributes:
        session: Active SQLAlchemy session used for queries and commits.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session.

        Args:
            session: SQLAlchemy Session instance.
        """
        self.session = session

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Fetch a single project by its primary key.

        Args:
            project_id: Project identifier.
        Returns:
            The Project instance if found; otherwise None.
        """
        return self.session.query(Project).filter(Project.id == project_id).first()

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """Fetch a single project by its exact name.

        Args:
            project_name: Project name to match.
        Returns:
            The Project instance if found; otherwise None.
        """
        return self.session.query(Project).filter(Project.name == project_name).first()

    def add_project(self, project: Project) -> None:
        """Persist a new project.

        Args:
            project: Project instance to add.
        """
        self.session.add(project)
        self.session.commit()

    def delete_project(self, project: Project) -> None:
        """Delete an existing project.

        Args:
            project: Project instance to delete.
        """
        self.session.delete(project)
        self.session.commit()

    def set_project_name(self, project: Project, new_project_name: str) -> None:
        """Update a project's name and commit.

        Args:
            project: Project to update.
            new_project_name: New name value.
        """
        project.name = new_project_name
        self.session.commit()

    def set_project_description(self, project: Project, new_project_description: str) -> None:
        """Update a project's description and commit.

        Args:
            project: Project to update.
            new_project_description: New description value.
        """
        project.description = new_project_description
        self.session.commit()

    def project_tasks_list(self, project: Project) -> List["Task"]:
        """List tasks associated with a project.

        Args:
            project: Project whose tasks to list.
        Returns:
            A list of Task objects linked to the project.
        """
        return list(project.tasks)

    def all_projects(self) -> List[Type[Project]]:
        """Return all projects.

        Returns:
            A list of all Project objects.
        """
        return list(self.session.query(Project))
