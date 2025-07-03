from app.models.basemodel import BaseModel
from app import bcrypt
from datetime import datetime
from app import db

class User(BaseModel, db.Model):
    """
    Represents a user of the HBnB platform.

    Attributes:
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        password (str): User's hashed password (not returned in to_dict).
        is_admin (bool): Indicates if the user is an admin.
    """

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    # --- Properties ---

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name is required and must be less than 50 characters.")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name is required and must be less than 50 characters.")
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise ValueError("Valid email is required.")
        self.__email = value

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean.")
        self.__is_admin = value

    # --- Password ---

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) or len(value) < 8:
            raise ValueError("Password must be a string of at least 8 characters.")
        self.__password = value

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
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
