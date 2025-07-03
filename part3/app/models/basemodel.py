from datetime import datetime

class BaseModel:
    """Base class for all models (used as a mixin)"""

    def save(self):
        from app import db  # Local import avoids circular issue
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
