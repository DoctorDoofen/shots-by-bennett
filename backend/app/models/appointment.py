from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from .user import User


class Appointment (db.model):

    __tablename__ = "appointments"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "scheduled_time": self.scheduled_time.isoformat(),
            "user_id": self.user_id
        }
