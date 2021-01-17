import logging
from datetime import datetime
from typing import List


class User:
    _username: str
    _id: int
    _key: int
    _sign_ins: List[datetime]
    _registration_date: datetime
    _cleared_for_access: bool

    def __init__(self, attributes: List[str or int]):
        """ Attributes
        [0] username : str
        [1] key : int
        [2] id : int"""
        self._username = attributes[0]
        self._key = attributes[1]
        self._id = attributes[2]
        self._sign_ins = [datetime.now()]
        self._registration_date = datetime.now()
        self._cleared_for_access = True

    def get_attributes(self) -> List[str or int]:
        """Returns a user's attributes in a consistent order"""
        return [self._username, self._key, self._id]

    def add_sign_in(self):
        """Adds a date when this user signed in."""
        self._sign_ins.append(datetime.now())

    def has_access(self) -> bool:
        """Returns whether this user is cleared for access."""

    def restrict_access(self):
        """Marks this user as not cleared for access."""
        self._cleared_for_access = False

    @staticmethod
    def num_writable_attributes():
        """The number of attributes contained in a user"""
        return 3

    def get_username(self) -> str:
        """Returns this user's username"""
        return self._username

    def get_key(self):
        """Returns this user's key"""
        return self._key

    def get_id(self):
        """Returns this users ID"""
        return self._id

    def get_last_sign_in(self):
        """"Returns this users last sign in date"""
        logging.info(self._sign_ins)
        return self._sign_ins[-1]

    def get_sign_ins(self):
        """Gets the list of times this user has signed in"""
        return self._sign_ins
