from typing import BinaryIO
import logging
from user import User
from datetime import datetime
import Users
import pickle
import os.path
from login_exceptions import InvalidInput


def str_to_date(input_str: str) -> datetime:
    date = datetime.strptime(input_str, '%Y-%m-%d %H:%M:%S')
    return date


def date_to_str(input_date: datetime) -> str:
    return input_date.strftime('%Y-%m-%d %H:%M:%S')


class LogManager:

    latest_user_id: int
    base_path = os.path.join("Users")

    def __init__(self):
        filepath = os.path.join(self.base_path)
        lst = os.listdir(filepath)
        self.latest_user_id = len(lst) - 1

    def get_user_file_write(self, userid: int) -> BinaryIO:
        """Gets a read/write pickle file for a given user"""
        filepath = os.path.join(self.base_path, str(userid) + ".pickle")
        return open(filepath, "wb")

    def get_user_file_read(self, userid: int) -> BinaryIO:
        """Gets a read/write pickle file for a given user"""
        filepath = os.path.join(self.base_path, str(userid) + ".pickle")
        return open(filepath, "rb")

    def get_user(self, user_id: int, username: str) -> User:
        """Retrieves a user from the archives given their ID"""
        try:
            logging.info("Retrieving user" + str(user_id))
            uf = self.get_user_file_read(user_id)
            logging.info("User file received")
            user = pickle.load(uf)
            logging.info("User loaded")
            logging.info(user.get_attributes())
            logging.info(user.get_sign_ins())
            uf.close()
        except FileNotFoundError:
            raise InvalidInput("User specified does not exist")

        if user.get_username() != username:
            raise InvalidInput("Username does not match username on record: " +
                               user.get_username() + "!=" + username)
        return user

    def register_new_user(self, user: User):
        """Creates a new pickle for a given user"""
        logging.info("Registering new user")
        new_user_file = self.get_user_file_write(user.get_id())
        pickle.dump(user, new_user_file)
        logging.info("User stored")
        new_user_file.close()

    def get_new_user_id(self) -> int:
        """Creates a new and unique user id"""
        self.latest_user_id += 1
        return self.latest_user_id

    def add_tap_log(self, user_id: int):
        """Adds a log to the users tap record."""
        uf = self.get_user_file_read(user_id)
        user = pickle.load(uf)
        user.add_sign_in()
        uf = self.get_user_file_write(user.get_id())
        pickle.dump(user, uf)
        uf.close()

    def get_last_use(self, user_id: int) -> datetime:
        """Gets the last time a given user used this scanner."""
        uf = self.get_user_file_read(user_id)
        user = pickle.load(uf)
        date = user.get_last_sign_in()
        uf.close()
        return date

    def get_login_str(self, user: User) -> str:
        """Generates the message that is displayed when the user is logged in"""
        login_str = ""

        last_login = user.get_last_sign_in()

        time_since_last_login = (datetime.now() - last_login)

        time_since_last_login_str = str(time_since_last_login.days) + \
                                    " days & " + str(
            round(time_since_last_login.seconds / 3600)) + \
                                    " hrs ago"

        login_str += "Welcome back " + user.get_username() + "\n" + \
                     "Your last loginsystem was at:\n" + \
                     str(last_login.strftime("%b %d %Y %I:%M%p")) + "\n" + \
                     time_since_last_login_str

        return login_str
