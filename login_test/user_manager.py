import logging

from presenters import Presenter
from datetime import datetime
import RPi.GPIO as GPIO
from reader import Reader
from security_manager import SecurityManager
from user import User
from log_manager import LogManager


class InvalidInput(Exception):
    """Raised when input from the RFID tag does not match the expected
    formatting."""
    pass


class InvalidUserCode(Exception):
    """Raised when a user's code is invalid"""
    pass


class UserManager:
    reader: Reader
    presenter: Presenter
    security_manager: SecurityManager
    user_log_manager: LogManager

    def __init__(self, presenter: Presenter, reader: Reader, security_manager:
    SecurityManager, user_log_manager: LogManager):
        self.presenter = presenter
        self.reader = reader
        self.security_manager = security_manager
        self.user_log_manager = user_log_manager

    def register_new_user(self):
        """Prompts user to enter a username, then writes new user info to the
        RFID tag."""
        user_txt = self.presenter.input("Enter a username for the new user.")
        self.presenter.print("Now place your tag to write")
        new_user = self.create_new_user(user_txt)
        self.user_log_manager.register_new_user(new_user)
        self.write_user_to_tag(new_user)
        self.presenter.print("Welcome, " + user_txt)

    def write_user_to_tag(self, user: User):
        """Writes new user info to an RFID tag. Waits for a tag to contact.
        Written info format:
        'entered_username|last_login_datetime('%Y-%m-%d %H:%M:%S')' """
        attributes = user.get_attributes()
        user_info = ""

        for attribute in attributes:
            user_info += str(attribute)
            user_info += "|"

        user_info = user_info[0:-1]

        try:
            self.reader.write(user_info)
        finally:
            GPIO.cleanup()

    def user_from_input(self, user_data: str) -> User:
        """Returns a list of attributes extracted from an input string. Raises
        InvalidInput if the input does not match the expected formatting
        attributes at indexes:
        [0]: username
        [1]: user key
        [2]: unique user id
        separated by '|' """
        num_attributes = User.num_writable_attributes()
        attributes = []
        logging.info(user_data)
        try:
            for i in range(num_attributes):
                attributes += " "
            # print("made it")
            att_ind = 0
            for char in user_data:
                # print(char)
                if char == "|":
                    att_ind += 1
                else:
                    attributes[att_ind] += char
            logging.info(attributes)

            for i in range(num_attributes):
                attributes[i] = attributes[i].strip()

            logging.info(attributes)

            # Checking that the received input is valid
            if num_attributes - 1 != att_ind:
                logging.info(num_attributes, att_ind)
                raise InvalidInput

            logging.info("Valid input format")

            if not self.security_manager.validate_key(int(attributes[1])):
                logging.exception("Invalid Key:", attributes[1])
                raise InvalidUserCode

            logging.info("Valid Key")

            return self.user_log_manager.get_user(int(attributes[2]))
        except IndexError:
            logging.exception("IndexErr")
            raise InvalidInput
        except ValueError:
            logging.exception("ValueErr")
            raise InvalidInput
        # TODO add more specific error messages

    def create_new_user(self, username: str) -> User:
        """Creates a new user with a valid passkey"""
        return User([username, self.security_manager.generate_key(),
                     self.user_log_manager.get_new_user_id()])
