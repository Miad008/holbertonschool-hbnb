import uuid

class InMemoryStorage:
    def __init__(self):
        self.data = {
            "users": {},
            "places": {},
            "reviews": {},
            "amenities": {}
        }

    def generate_id(self):
        return str(uuid.uuid4())

    def add(self, entity_type, obj):
        if not hasattr(obj, 'id'):
            obj.id = self.generate_id()
        self.data[entity_type][obj.id] = obj
        return obj

    def get(self, entity_type, obj_id):
        return self.data[entity_type].get(obj_id)

    def get_all(self, entity_type):
        return list(self.data[entity_type].values())

    def delete(self, entity_type, obj_id):
        return self.data[entity_type].pop(obj_id, None)
