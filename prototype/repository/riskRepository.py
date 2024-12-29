from prototype.model.risk import Risk
from prototype.extensions import db

class RiskRepository:
    @staticmethod
    def get_risk_by_id(risk_id):
        return Risk.query.get(risk_id)
    
    @staticmethod
    def get_all():
        return Risk.query.all()
    
    @staticmethod
    def add_risk(category, criteria, risk_level, project_id):
        new_risk = Risk(category=category, risk_level=risk_level, criteria=criteria, project_id=project_id)
        db.session.add(new_risk)
        db.session.commit()
        return new_risk
    
    @staticmethod
    def delete_risk_by_id(Risk_id):
        Risk = RiskRepository.get_risk_by_id(Risk_id)
        if Risk:
            db.session.delete(Risk)
            db.session.commit()