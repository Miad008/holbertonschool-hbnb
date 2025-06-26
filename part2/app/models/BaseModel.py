import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all models in the application.

    Attributes:
        id (str): Unique identifier using UUID.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
    """

    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        now = datetime.utcnow()
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def update_timestamp(self):
        """Update the timestamp of the last modification."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update object attributes from a dictionary and refresh the updated_at timestamp.
        Ignores attributes that do not already exist on the object.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_timestamp()

    def to_dict(self):
        """Return a dictionary representation of the instance (JSON-ready)."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
