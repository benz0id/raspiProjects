from Presenter import Presenter
from datetime import datetime
import RPi.GPIO as GPIO
from Reader import Reader
from SecurityManager import SecurityManager
from User import User


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

    def __init__(self, presenter: Presenter, reader: Reader, security_manager:
                 SecurityManager):
        self.presenter = presenter
        self.reader = reader
        self.security_manager = security_manager

    def register_new_user(self):
        """Prompts user to enter a username, then writes new user info to the
        RFID tag."""
        user_txt = self.presenter.input("Enter a username for the new user.")
        self.presenter.print("Now place your tag to write")
        new_user = self.create_new_user(user_txt)
        self.write_user_to_tag(new_user)
        self.presenter.print("Welcome, " + user_txt)

    def write_user_to_tag(self, user: User):
        """Writes new user info to an RFID tag. Waits for a tag to contact.
        Written info format:
        'entered_username|last_login_datetime('%Y-%m-%d %H:%M:%S')' """
        attributes = [
            user.get_username(),
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            str(user.get_key()),
        ]
        user_info = ""

        for attribute in attributes:
            user_info += attribute
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
        [1]: last login datetime
        [2]: unique user key
        separated by '|' """
        num_attributes = 3
        attributes = []
        print(user_data)
        try:
            for i in range(num_attributes):
                attributes += ""

            att_ind = 0
            for char in user_data:
                if char == "|":
                    att_ind += 1
                else:
                    attributes[att_ind] += char
            print(attributes)

            # Checking that the received input is valid
            if num_attributes - 1 != att_ind:
                print(num_attributes, att_ind)
                raise InvalidInput

            if self.security_manager.validate_key(int(attributes[2])):
                print("Invalid Key:", attributes[2])
                raise InvalidUserCode

            for i in range(len(attributes)):
                attributes[i] = attributes[i].strip()

            User.str_to_date(attributes[1])

            return User(attributes[0], User.str_to_date(attributes[1]),
                        attributes[2])
        except IndexError:
            print("IndexErr")
            raise InvalidInput
        except ValueError:
            print("ValueErr")
            raise InvalidInput

    def create_new_user(self, username: str) -> User:
        """Creates a new user with a valid passkey"""
        return User(username, datetime.now(),
                    self.security_manager.generate_key())
