from prototype.model.project import Project
from prototype.extensions import db
from sqlalchemy.orm.exc import NoResultFound

class ProjectRepository:
    @staticmethod
    def get_project_by_id(project_id: int) -> Project:
        return Project.query.get(project_id)
    
    @staticmethod
    def get_project_by_name(project_name: str) -> Project:
        return Project.query.filter_by(name=project_name).first()
    
    @staticmethod
    def get_all():
        return Project.query.all()
    
    @staticmethod
    def add_project(name: str) -> Project:
        project = Project(name=name)
        db.session.add(project)
        db.session.commit()
        return project

    @staticmethod
    def update_counts(project_id: int, low_risks=None, med_risks=None, high_risks=None):
        try:
            project: Project = Project.query.get_or_404(project_id)
            project.low_risks = low_risks
            project.medium_risks = med_risks
            project.high_risks = high_risks
            db.session.commit()
        except:
            raise RuntimeError(f"Project with id {project_id} not found.")
    
    @staticmethod
    def delete_project_by_id(project_id: int):
        try:
            project = Project.query.filter_by(id=project_id).one()  # Use one() to raise an exception if not found
            db.session.delete(project)
            db.session.commit()
        except NoResultFound:
            # Handle the case where the project doesn't exist.
            # Example: raise a custom exception or log a warning.
            raise RuntimeError(f"Project with id {project_id} not found.")
    