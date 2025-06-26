from app.models.base import BaseModel

class Amenity(BaseModel):
    """
    Represents a feature or amenity offered in a place.

    Attributes:
        name (str): Name of the amenity (required, max 50 characters).
        description (str): Optional description.
        places (list): Optional list of places where this amenity is used.
    """

    def __init__(self, name, description="", id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.description = description
        self.places = []  # Optional reverse relation (not required by spec)

    # --- Property with validation ---
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Amenity name is required and must be less than 50 characters.")
        self.__name = value

    # --- Optional relation ---
    def add_place(self, place):
        """Link this amenity to a place (optional, not required in spec)."""
        self.places.append(place)

    # --- Serialization ---
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "description": self.description,
            "places": [p.id if hasattr(p, "id") else p for p in self.places]
        })
        return base_dict
