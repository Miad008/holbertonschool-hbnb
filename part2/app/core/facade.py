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

    def delete_user(self, user_id):
        """يحذف مستخدم حسب ID"""
        return self.storage.delete("users", user_id)
