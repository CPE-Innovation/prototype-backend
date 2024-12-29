from prototype.extensions import db
import datetime

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    high_risks = db.Column(db.Integer, default=0)
    medium_risks = db.Column(db.Integer, default=0)
    low_risks = db.Column(db.Integer, default=0)
    critical = db.Column(db.Boolean, default=False, nullable=False)
    severity = db.Column(db.String(4), default="LOW", nullable=False)

    def __repr__(self):
        return f"<Project {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "high_risks": self.high_risks,
            "medium_risks": self.medium_risks,
            "low_risks": self.low_risks,
            "critical": self.critical,
            "severity": self.severity
        }