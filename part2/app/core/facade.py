from app.repository.in_memory_storage import InMemoryStorage

class HBnBFacade:
    def __init__(self):
        self.storage = InMemoryStorage()

    # ----- User Methods -----
    def create_user(self, user_data):
        from app.core.models.user import User
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
        from app.core.models.amenity import Amenity
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
        from app.core.models.place import Place
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
