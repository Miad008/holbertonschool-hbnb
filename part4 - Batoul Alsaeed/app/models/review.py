from app.models.base import BaseModel
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Review(BaseModel):
    """
    Represents a review made by a user for a place.

    Attributes:
        text (str): The content of the review (required).
        rating (int): Rating between 1 and 5 (optional).
        user_id (str): ID of the user who wrote the review.
        place_id (str): ID of the place being reviewed.
    """

    __tablename__ = 'reviews'

    _text     = db.Column(db.Text,    nullable=False)
    _rating   = db.Column(db.Integer, nullable=True)
    _user_id  = db.Column(db.String(36), db.ForeignKey('users.id'),  nullable=False)
    _place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # --- Relationships for Task 8 ---
    user  = db.relationship(
        'User',
        back_populates='reviews'
    )
    place = db.relationship(
        'Place',
        back_populates='reviews'
    )

    def __init__(self, text, user, place, rating=None, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        if not text:
            raise ValueError("Review text is required.")
        if not hasattr(user, "id"):
            raise ValueError("User must be a valid object with an ID.")
        if not hasattr(place, "id"):
            raise ValueError("Place must be a valid object with an ID.")

        self.text   = text
        self.user   = user
        self.place  = place
        self._rating = None
        self.rating = rating  # uses setter for validation

    # --- Properties with validation ---

    @hybrid_property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string.")
        if len(value) > 1024:
            raise ValueError("Review text must be ≤ 1024 characters.")
        self._text = value

    @hybrid_property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value is not None:
            if not isinstance(value, int) or not (1 <= value <= 5):
                raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value

    @hybrid_property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError("User ID must be a valid UUID string.")
        self._user_id = value

    @hybrid_property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError("Place ID must be a valid UUID string.")
        self._place_id = value

    # --- Serialization ---

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "text":     self.text,
            "rating":   self.rating,
            "user_id":  self.user.id  if hasattr(self, "user")  else None,
            "place_id": self.place.id if hasattr(self, "place") else None
        })
        return base
