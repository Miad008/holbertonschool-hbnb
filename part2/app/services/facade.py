from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- User Methods -----
    def create_user(self, user_data):
        from app.models.user import User  
        new_user = User(**user_data)
        return self.user_repo.add(new_user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.update_timestamp()
        return user

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ----- Amenity Methods -----
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        if not amenity_data.get("name"):
            raise ValueError("Missing required amenity fields")
        new_amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(new_amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, updated_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        for key, value in updated_data.items():
            setattr(amenity, key, value)
        return amenity

    # ----- Place Methods -----
    def create_place(self, place_data):
        from app.models.place import Place
        required_fields = ["name", "address", "owner_id", "price"]
        if not all(field in place_data and place_data[field] for field in required_fields):
            raise ValueError("Missing required place fields")
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, updated_data):
        place = self.get_place(place_id)
        if not place:
            return None
        for key, value in updated_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        place.update_timestamp()
        return place

    # ----- Review Methods -----
    def create_review(self, review_data):
        from app.models.review import Review
        required_fields = ["user_id", "place_id", "text"]
        if not all(field in review_data and review_data[field] for field in required_fields):
            raise ValueError("Missing required review fields")
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, updated_data):
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in updated_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        review.update_timestamp()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return None
        place = self.get_place(review.place_id)
        if place and review_id in place.review_ids:
            place.review_ids.remove(review_id)
        return self.review_repo.delete(review_id)
