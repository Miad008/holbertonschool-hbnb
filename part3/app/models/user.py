from app.models.basemodel import BaseModel
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

     # --- Relationships for Task 8 ---
    places  = db.relationship(
        'Place',
        back_populates='owner',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    reviews = db.relationship(
        'Review',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def hash_password(self, password):
        """Hashes and sets the user's password"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if a password matches the stored hash"""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Return a dictionary representation of the user (excluding password)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
