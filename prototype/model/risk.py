from prototype.extensions import db
import datetime

class Risk(db.Model):
    __tablename__ = "risks"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), nullable=False)
    criteria = db.Column(db.String(50), nullable=False)
    risk_level = db.Column(db.String(4), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<Risk {self.criteria} of category {self.category}>"
    
    def serialize(self):
        return {
            "id": self.id, 
            "category": self.category, 
            "criteria": self.criteria, 
            "project_id": self.project_id,
            "created_at": self.created_at
            }