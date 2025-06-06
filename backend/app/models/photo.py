from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Photo(db.model):

    __tablename__ = 'photos'

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.now())

