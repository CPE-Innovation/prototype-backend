from prototype.repository.projectRepository import ProjectRepository
from prototype.repository.riskRepository import RiskRepository

class ProjectService:
    @staticmethod
    def getProject(project_id):
        return ProjectRepository.get_project_by_id(project_id)
    
    @staticmethod
    def addProject(name):
        return 
    
    def getRisks(project_id):
        return # Risk[]