from app.repository.in_memory_storage import InMemoryStorage

class HBnBFacade:
    def __init__(self):
        self.storage = InMemoryStorage()

    # ----- User Methods -----
    def create_user(self, user_data):
        from app.models.user import User  
        new_user = User(**user_data)
        return self.storage.add("users", new_user)

    def get_user(self, user_id):
        return self.storage.get("users", user_id)

    def get_all_users(self):
        return self.storage.get_all("users")

    def update_user(self, user_id, user_data):
        user = self.storage.get("users", user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.update_timestamp()
        return user

    def delete_user(self, user_id):
        return self.storage.delete("users", user_id)

    # ----- Amenity Methods -----
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        new_amenity = Amenity(**amenity_data)
        return self.storage.add("amenities", new_amenity)

    def get_amenity(self, amenity_id):
        return self.storage.get("amenities", amenity_id)

    def get_all_amenities(self):
        return self.storage.get_all("amenities")

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
        new_place = Place(**place_data)
        return self.storage.add("places", new_place)

    def get_place(self, place_id):
        return self.storage.get("places", place_id)

    def get_all_places(self):
        return self.storage.get_all("places")

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
        """ينشئ تقييم جديد ويربطه بمكان"""
        from app.models.review import Review
        new_review = Review(**review_data)
        self.storage.add("reviews", new_review)

        # ربط التقييم بالمكان
        place = self.get_place(new_review.place_id)
        if place:
            place.review_ids.append(new_review.id)
        return new_review

    def get_review(self, review_id):
        """يرجع تقييم حسب ID"""
        return self.storage.get("reviews", review_id)

    def get_all_reviews(self):
        """يرجع كل التقييمات"""
        return self.storage.get_all("reviews")

    def update_review(self, review_id, updated_data):
        """تحديث بيانات التقييم"""
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in updated_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        review.update_timestamp()
        return review

    def delete_review(self, review_id):
        """يحذف التقييم ويربطه بالمكان الصحيح"""
        review = self.get_review(review_id)
        if not review:
            return None

        place = self.get_place(review.place_id)
        if place and review_id in place.review_ids:
            place.review_ids.remove(review_id)

        return self.storage.delete("reviews", review_id)
