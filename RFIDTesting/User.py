from datetime import datetime
from typing import List
import logging


class User:
    __username: str
    __id: int
    __key: int
    __sign_ins: List[datetime]
    __registration_date: datetime

    def __init__(self, attributes: List[str or int]):
        """ Attributes
        [0] username : str
        [1] key : int
        [2] id : int"""
        self.__username = attributes[0]
        self.__key = attributes[1]
        self.__id = attributes[2]
        self.__sign_ins = [datetime.now()]
        self.__registration_date = datetime.now()

    def get_attributes(self) -> List[str or int]:
        """Returns a user's attributes in a consistent order"""
        return [self.__username, self.__key, self.__id]

    def add_sign_in(self):
        """Adds a date when this user signed in."""
        self.__sign_ins.append(datetime.now())

    @staticmethod
    def num_writable_attributes():
        """The number of attributes contained in a user"""
        return 3

    def get_username(self) -> str:
        """Returns this user's username"""
        return self.__username

    def get_key(self):
        """Returns this user's key"""
        return self.__key

    def get_id(self):
        """Returns this users ID"""
        return self.__id

    def get_last_sign_in(self):
        """"Returns this users last sign in date"""
        logging.info(self.__sign_ins)
        return self.__sign_ins[-1]

    def get_sign_ins(self):
        """Gets the list of times this user has signed in"""
        return self.__sign_ins
