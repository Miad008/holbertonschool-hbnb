import uuid

class InMemoryStorage:
    def __init__(self):
        # تخزين كل نوع من البيانات في قاموس خاص فيه
        self.data = {
            "users": {},
            "places": {},
            "reviews": {},
            "amenities": {}
        }

    def generate_id(self):
        """ينتج ID فريد باستخدام uuid4"""
        return str(uuid.uuid4())

    def add(self, entity_type, obj):
        """يضيف كائن إلى التخزين"""
        if not hasattr(obj, 'id'):
            obj.id = self.generate_id()
        self.data[entity_type][obj.id] = obj
        return obj

    def get(self, entity_type, obj_id):
        """يرجع كائن معين حسب النوع والـ ID"""
        return self.data[entity_type].get(obj_id)

    def get_all(self, entity_type):
        """يرجع جميع الكائنات من نوع معين"""
        return list(self.data[entity_type].values())

    def delete(self, entity_type, obj_id):
        """يحذف كائن حسب النوع والـ ID"""
        return self.data[entity_type].pop(obj_id, None)
