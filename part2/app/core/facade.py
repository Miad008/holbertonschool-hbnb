from app.repository.in_memory_storage import InMemoryStorage

class HBnBFacade:
    def __init__(self):
        self.storage = InMemoryStorage()

    def create_user(self, user_data):
        """ينشئ مستخدم جديد ويخزّنه"""
        from app.core.models.user import User
        new_user = User(**user_data)
        return self.storage.add("users", new_user)

    def get_user(self, user_id):
        """يرجع مستخدم حسب ID"""
        return self.storage.get("users", user_id)

    def get_all_users(self):
        """يرجع كل المستخدمين"""
        return self.storage.get_all("users")

    def update_user(self, user_id, user_data):
    """تحديث بيانات المستخدم حسب ID"""
    user = self.storage.get("users", user_id)
    if not user:
        return None
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    user.update_timestamp()
    return user

    def delete_user(self, user_id):
        """يحذف مستخدم حسب ID"""
        return self.storage.delete("users", user_id)

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
