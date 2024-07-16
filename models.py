import os
from flask_login import UserMixin


class User(UserMixin):
    _id = os.getenv("SECRET_ID")
    def __init__(self):
        self._username = os.getenv("SECRET_KEY")
        self._password = os.getenv("SECRET_PASS")

    @property
    def get_username(self):
        return self._username

    @property
    def get_password(self):
        return self._password

    @classmethod
    def get_id(self):
        return self._id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

