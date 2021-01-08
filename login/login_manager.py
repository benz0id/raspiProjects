import logging

from devices.reader import Reader
from .log_record_manager import LogManager
from .login_exceptions import InvalidInput, InvalidUserCode
from .presenters import ConsolePresenter, Presenter
from .security_manager import SecurityManager
from .user import User
from .user_manager import UserManager

logging.basicConfig(filename="logs.log", level= logging.DEBUG)

# User String Format:
# "username | user_code | user_id"
# Designed for use with rc522 module, wired as required by the mfrc522 module


class LoginManager:

    _security_manager: SecurityManager
    _reader: Reader
    _presenter: Presenter
    _user_log_manager: LogManager
    _user_manager: UserManager

    def __init__(self, reader: Reader,
                 presenter: Presenter = ConsolePresenter()):
        """Creates a new LoginManager with a certain presenter strategy"""
        self._security_manager = SecurityManager()
        self._reader = reader
        self._presenter = presenter
        self._user_log_manager = LogManager()
        self._user_manager = UserManager(presenter, self._reader,
                                         self._security_manager,
                                         self._user_log_manager)

    def run_login_system(self) -> int:
        """Runs the login system system, returns a userID if found"""
        self._user_manager.register_new_user()
        # Main loop
        # Fetch any data available from the RFID reader
        data = self._reader.get_tag_data()
        valid_user = self.check_for_user(data)
        if valid_user:
            self.run_sign_in_process(valid_user)

        return valid_user.get_id()

    def add_new_user(self):
        """Adds a new user to the directory"""
        self._user_manager.register_new_user()

    def check_for_user(self, input_data: str) -> bool or User:
        """Checks if the data is a valid users' data. Shows corresponding error
        messages iff the user's data isn't formatted properly."""
        try:
            user = self._user_manager.user_from_input(input_data)
            return user
        except InvalidInput:
            logging.exception(InvalidInput)
            self._presenter.print("Bad Read or Invalid Key")
        except InvalidUserCode:
            logging.exception(InvalidUserCode)
            self._presenter.print("User code invalid")
        return False

    def run_sign_in_process(self, user: User):
        """Runs the series of events that should occur when a user taps onto the
        reader."""
        self._presenter.print(self._user_log_manager.get_login_str(user))
        self._user_log_manager.add_tap_log(user)
