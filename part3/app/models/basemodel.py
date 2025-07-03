from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base class for all models"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
