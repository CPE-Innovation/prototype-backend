from prototype.services.model_steps.processing import Processing, CriticityLevel
from prototype.services.model_steps.preprocessing import Preprocessing_APITest # A terme, abstraction IPreprocessing et LSP/DIP
from prototype.repository.riskRepository import RiskRepository
from prototype.repository.projectRepository import ProjectRepository
from concurrent.futures import ThreadPoolExecutor
from flask import current_app

class ModelService:

    # Dans le futur, ceci suivra un patterne décorateur : on rajoute dynamiquement les fetchs souhaités, les uns à la suite des autres
    @staticmethod
    def fetch_data():
        # message = {"PROJECT", "MESSAGE", "ORIGIN", "DATE"}
        print("Fetching Data...")
        messages = Preprocessing_APITest.preprocess()
        print("Done !")
        print("Processing messages...")

        with current_app.app_context():  #parallelisme
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(
                    executor.map(
                        lambda msg: ModelService.__workflow_with_context(msg), messages
                    )
                )
        print("Done !")
        return

    @staticmethod
    def __workflow_with_context(message):
        # Assurez-vous qu'un contexte Flask est disponible dans chaque thread
        with current_app.app_context():
            return ModelService.__workflow(message)

    @staticmethod
    def __workflow(message):
        # Get project
        project = ProjectRepository.get_project_by_name(message["PROJECT"])
        if not project:
            project = ProjectRepository.add_project(message["PROJECT"])
        risks = Processing.analyze_risks(message["MESSAGE"])
        # Add risks
        counts = {
            CriticityLevel.LOW.value : 0,
            CriticityLevel.MEDIUM.value : 0,
            CriticityLevel.HIGH.value : 0
            }
        for risk in risks:
            RiskRepository.add_risk(risk["CATEGORY"], risk["CRITERIA"], risk["RISK_LEVEL"], project.id)
            counts[risk["RISK_LEVEL"]] += 1
        # Update project
        ProjectRepository.update_counts(project.id, counts[CriticityLevel.LOW.value], 
                                        counts[CriticityLevel.MEDIUM.value], counts[CriticityLevel.HIGH.value])
        return
