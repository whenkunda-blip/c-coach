from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_text = db.Column(db.Text)
    job_description = db.Column(db.Text)
    extracted_skills = db.Column(db.JSON)  # User's current skills
    required_skills = db.Column(db.JSON)   # Job requirements
    skill_gaps = db.Column(db.JSON)        # Calculated gaps
    readiness_score = db.Column(db.Float)  # Overall match percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ActionPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    tasks = db.Column(db.JSON)             # Generated tasks
    completed_tasks = db.Column(db.JSON, default=[])
    updated_readiness_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
