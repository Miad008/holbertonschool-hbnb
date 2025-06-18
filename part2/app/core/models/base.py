import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        now = datetime.utcnow()
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def update_timestamp(self):
        """يحدث وقت آخر تعديل"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """يرجع الكائن على شكل قاموس (JSON-ready)"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
