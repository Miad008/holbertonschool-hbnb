from app.core.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name  # اسم الميزة مثل "WiFi", "Kitchen", إلخ

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name
        })
        return base_dict
