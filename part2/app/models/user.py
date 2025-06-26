from app.models.BaseModel import BaseModel
from datetime import datetime

class User(BaseModel):
    """
    Represents a user of the HBnB platform.

    Attributes:
        first_name (str): User's first name (required, max 50 characters).
        last_name (str): User's last name (required, max 50 characters).
        email (str): User's email address (required, valid format).
        is_admin (bool): Indicates if the user is an admin. Defaults to False.
    """

    def __init__(self, first_name, last_name, email, is_admin=False, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

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

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        
