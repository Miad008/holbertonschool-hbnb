class User:
    def __init__(self, first_name, last_name, email, id=None):
        self.id = id  # ممكن يجي من الخارج أو يتم توليده داخل التخزين
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        """يرجع البيانات كقاموس (JSON ready)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
