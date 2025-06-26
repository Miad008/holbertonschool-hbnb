from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- USER ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.update_timestamp()
        return user

    # --- AMENITY ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "")
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be ≤ 50 characters.")
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        for key, value in data.items():
            setattr(amenity, key, value)
        return amenity

    # --- PLACE ---
    def create_place(self, place_data):
        # Validation
        price = place_data.get("price")
        lat = place_data.get("latitude")
        lng = place_data.get("longitude")

        if price is None or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if lat is None or not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if lng is None or not (-180 <= lng <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        # Owner validation
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found.")

        # Amenities (if provided)
        amenity_objs = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenity_objs.append(amenity)

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=price,
            latitude=lat,
            longitude=lng,
            owner=owner,
            amenities=amenity_objs
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None

        # Validation
        if "price" in data and data["price"] < 0:
            raise ValueError("Price must be non-negative.")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            raise ValueError("Latitude out of bounds.")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            raise ValueError("Longitude out of bounds.")
        if "owner_id" in data:
            owner = self.user_repo.get(data["owner_id"])
            if not owner:
                raise ValueError("Owner not found.")
            place.owner = owner
            data.pop("owner_id")
        if "amenities" in data:
            amenities = []
            for amenity_id in data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities
            data.pop("amenities")

        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        place.update_timestamp()
        return place

    # --- REVIEW ---
    def create_review(self, review_data):
        required = ["user_id", "place_id", "text"]
        if not all(k in review_data and review_data[k] for k in required):
            raise ValueError("Missing review fields")

        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if not user or not place:
            raise ValueError("Invalid user or place")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        review.update_timestamp()
        return review

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- USER ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.update_timestamp()
        return user

    # --- AMENITY ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "")
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be ≤ 50 characters.")
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        for key, value in data.items():
            setattr(amenity, key, value)
        return amenity

    # --- PLACE ---
    def create_place(self, place_data):
        # Validation
        price = place_data.get("price")
        lat = place_data.get("latitude")
        lng = place_data.get("longitude")

        if price is None or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if lat is None or not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if lng is None or not (-180 <= lng <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        # Owner validation
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found.")

        # Amenities (if provided)
        amenity_objs = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenity_objs.append(amenity)

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=price,
            latitude=lat,
            longitude=lng,
            owner=owner,
            amenities=amenity_objs
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None

        # Validation
        if "price" in data and data["price"] < 0:
            raise ValueError("Price must be non-negative.")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            raise ValueError("Latitude out of bounds.")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            raise ValueError("Longitude out of bounds.")
        if "owner_id" in data:
            owner = self.user_repo.get(data["owner_id"])
            if not owner:
                raise ValueError("Owner not found.")
            place.owner = owner
            data.pop("owner_id")
        if "amenities" in data:
            amenities = []
            for amenity_id in data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities
            data.pop("amenities")

        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        place.update_timestamp()
        return place

    # --- REVIEW ---
    def create_review(self, review_data):
        required = ["user_id", "place_id", "text"]
        if not all(k in review_data and review_data[k] for k in required):
            raise ValueError("Missing review fields")

        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if not user or not place:
            raise ValueError("Invalid user or place")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        review.update_timestamp()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return None
        return self.review_repo.delete(review_id)
