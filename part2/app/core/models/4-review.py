from app.core.models.base import BaseModel

class Review(BaseModel):
    """
    Represents a review made by a user for a place.

    Attributes:
        text (str): The content of the review.
        user_id (str): ID of the user who made the review.
        place_id (str): ID of the place being reviewed.
        rating (int, optional): Rating from 1 to 5.
    """

    def __init__(self, text, user_id, place_id, rating=None, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.text = text
        self.user_id = user_id  # صاحب التقييم
        self.place_id = place_id  # المكان الذي تم تقييمه
        
        if rating is not None:
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
        self.rating = rating

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "text": self.text,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating
        })
        return base_dict
