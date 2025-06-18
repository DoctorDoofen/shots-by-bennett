from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from .user import User

class Review (db.Model):
    __tablename__ = "reviews"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.Text, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        created_at = db.Column(db.DateTime, default=db.func.now())

        user = db.relationship("User", back_populates="reviews", cascade="all, delete")

        def to_dict(self):
            return {
                "id": self.id,
                "text": self.text,
                "user_id": self.user_id,
                "created_at": self.created_at.isoformat()
            }