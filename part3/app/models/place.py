from app.models.base import BaseModel
from app import db
import uuid

class Place(BaseModel):
    """
    Represents a place listed by a user.

    Attributes:
        title (str): Title of the place (max 100 characters).
        description (str): Optional description.
        price (float): Price per night (must be ≥ 0).
        latitude (float): Must be between -90 and 90.
        longitude (float): Must be between -180 and 180.
        owner (User): The user who owns the place.
        amenities (list): List of Amenity objects or IDs.
        reviews (list): List of Review objects or IDs.
    """

    __tablename__ = 'places'

    _title       = db.Column(db.String(100), nullable=False)
    _description = db.Column(db.String(500), nullable=True)
    _price       = db.Column(db.Float,    nullable=False)
    _latitude    = db.Column(db.Float,    nullable=False)
    _longitude   = db.Column(db.Float,    nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner,
                 amenities=None, reviews=None, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = amenities if amenities else []
        self.reviews = reviews if reviews else []

    # --- Properties with validation ---

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and must be less than 100 characters.")
        self.__title = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be a non-negative number.")
        self.__price = float(value)

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self.__latitude = float(value)

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self.__longitude = float(value)

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if not hasattr(value, "id"):
            raise ValueError("Owner must be a valid User object.")
        self.__owner = value

    # --- Methods ---

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": {
                "id": getattr(self.owner, "id", None),
                "first_name": getattr(self.owner, "first_name", ""),
                "last_name": getattr(self.owner, "last_name", ""),
                "email": getattr(self.owner, "email", "")
            } if self.owner else None,
            "amenities": [
                {"id": a.id, "name": getattr(a, "name", "")} if hasattr(a, "id") else {"id": a}
                for a in self.amenities
            ],
            "reviews": [r.id if hasattr(r, "id") else r for r in self.reviews]
        })
        return base_dict
