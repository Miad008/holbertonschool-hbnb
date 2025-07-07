from app.models.base import BaseModel
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Amenity(BaseModel):
    """
    Represents a feature or amenity offered in a place.

    Attributes:
        name (str): Name of the amenity (required, max 50 characters).
    """

    __tablename__ = 'amenities'

    _name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name

    # --- Property with validation ---

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name must be a non-empty string.")
        if len(value) > 50:
            raise ValueError("Amenity name must be ≤ 50 characters.")
        self._name = value

    # --- Serialization ---

    def to_dict(self):
        base = super().to_dict()
        base.update({"name": self.name})
        return base
