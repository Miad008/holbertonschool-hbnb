from app.models.base import BaseModel

class Amenity(BaseModel):
    """
    Represents a feature or amenity offered in a place.

    Attributes:
        name (str): Name of the amenity (e.g., WiFi, Pool).
    """

    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name  # اسم الميزة مثل "WiFi", "Kitchen", إلخ
	self.description = description

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
	"name": self.name,
	"description": self.description
        })
        return base_dict
