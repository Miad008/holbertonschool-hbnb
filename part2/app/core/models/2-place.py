from app.core.models.base import BaseModel

class Place(BaseModel):
    """
    Represents a place listed by a user.

    Attributes:
        name (str): Name of the place.
        description (str): Description of the place.
        address (str): Physical address of the place.
        owner_id (str): ID of the user who owns the place.
        amenity_ids (list): List of Amenity IDs associated with the place.
        review_ids (list): List of Review IDs associated with the place.
    """
    
    def __init__(self, name, description, address, owner_id, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.description = description
        self.address = address
        self.owner_id = owner_id  # ID خاص بالمستخدم الذي يملك هذا المكان
        self.amenity_ids = []     # قائمة IDs للأشياء المرتبطة
        self.review_ids = []      # قائمة IDs للتقييمات المرتبطة

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "owner_id": self.owner_id,
            "amenity_ids": self.amenity_ids,
            "review_ids": self.review_ids
        })
        return base_dict
