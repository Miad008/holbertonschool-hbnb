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

    def to_dict(self):
        """Return a dictionary representation of the instance (JSON-ready)."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
