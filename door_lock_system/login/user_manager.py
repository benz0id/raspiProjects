import logging
from datetime import datetime

from ..devices.reader import Reader
from .log_record_manager import LogManager
from .login_exceptions import InvalidInput, InvalidUserCode
from ..devices.presenters import Presenter
from .security_manager import SecurityManager
from .user import User


def get_user_data(user: User):
    """Gets a string representation of the user's info"""
    user_info = ""
    attributes = user.get_attributes()

    for attribute in attributes:
        user_info += str(attribute)
        user_info += "|"

    return user_info[0:-1]


def get_login_str(user: User) -> str:
    """Generates the message that is displayed when the user is logged in"""
    login_str = ""

    last_login = user.get_last_sign_in()

    time_since_last_login = (datetime.now() - last_login)

    time_since_last_login_str = str(time_since_last_login.days) + \
                                " days & " + str(
        round(time_since_last_login.seconds / 3600)) + \
                                " hrs ago"

    login_str += "Welcome back " + user.get_username() + "\n" + \
                 "Your last login was at:\n" + \
                 str(last_login.strftime("%b %d %Y %I:%M%p")) + "\n" + \
                 time_since_last_login_str

    return login_str


class UserManager:
    """A class that handles operations on and with users"""
    _reader: Reader
    _presenter: Presenter
    _security_manager: SecurityManager
    _user_log_manager: LogManager

    _recent_user: User

    def __init__(self, presenter: Presenter, reader: Reader, security_manager:
                 SecurityManager, user_log_manager: LogManager):
        self._presenter = presenter
        self._reader = reader
        self._security_manager = security_manager
        self._user_log_manager = user_log_manager

    def check_for_user(self, input_data: str) -> bool or User:
        """Checks if the data is a valid users' data. Shows corresponding error
        messages iff the user's data isn't formatted properly."""
        try:
            user = self.user_from_input(input_data)
            self._recent_user = user
            return True
        except InvalidInput:
            logging.exception(InvalidInput)
            self._presenter.print("Bad Read or Invalid Key")
        except InvalidUserCode:
            logging.exception(InvalidUserCode)
            self._presenter.print("User code invalid")
        return False

    def register_new_user(self):
        """Prompts user to enter a username, then writes new user info to the
        RFID tag."""
        user_txt = self._presenter.input("Enter a username for the new user.")
        self._presenter.print("Now place your tag to write")
        new_user = self.create_new_user(user_txt)
        self._user_log_manager.register_new_user(new_user)
        self.write_user_to_tag(new_user)
        self._presenter.print("Welcome, " + user_txt)

    def write_user_to_tag(self, user: User):
        """Writes new user info to an RFID tag. Waits for a tag to contact."""
        user_info = get_user_data(user)
        self._reader.write(str(user_info))

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
                logging.debug(str(num_attributes) + str(att_ind))
                raise InvalidInput

            logging.info("Valid input format")

            if not self._security_manager.validate_key(int(attributes[1])):
                logging.exception("Invalid Key:", attributes[1])
                raise InvalidUserCode

            logging.info("Valid Key")

            return self._user_log_manager.get_user(int(attributes[2]),
                                                   attributes[0])
        except IndexError:
            logging.exception(IndexError)
            raise InvalidInput
        except ValueError:
            logging.exception(ValueError)
            raise InvalidInput
        # TODO add more specific error messages

    def create_new_user(self, username: str) -> User:
        """Creates a new user with a valid passkey"""
        return User([username, self._security_manager.generate_key(),
                     self._user_log_manager.get_new_user_id()])

    def get_cur_login_str(self):
        """Returns the most recently logged in user's login str"""
        return get_login_str(self._recent_user)

    def get_cur_user_id(self) -> int:
        """Gets the most recently logged in user's id"""
        return self._recent_user.get_id()
