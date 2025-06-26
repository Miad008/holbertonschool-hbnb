from app.models.base import BaseModel

class Review(BaseModel):
    """
    Represents a review made by a user for a place.

    Attributes:
        text (str): The content of the review (required).
        rating (int): Rating between 1 and 5 (optional).
        user (User): The user who wrote the review.
        place (Place): The place being reviewed.
    """

    def __init__(self, text, user, place, rating=None, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        if not text:
            raise ValueError("Review text is required.")
        if not hasattr(user, "id"):
            raise ValueError("User must be a valid object with an ID.")
        if not hasattr(place, "id"):
            raise ValueError("Place must be a valid object with an ID.")

        self.text = text
        self.user = user
        self.place = place
        self._rating = None
        self.rating = rating  # Uses property for validation

    # --- Property with validation ---
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value is not None:
            if not isinstance(value, int) or not (1 <= value <= 5):
                raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value

    # --- Serialization ---
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None
        })
        return base_dict
