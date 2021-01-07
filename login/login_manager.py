from devices.reader import Reader
from presenters import SimplePresenter, Presenter
from security_manager import SecurityManager
from user_manager import UserManager
from user import User
from login_exceptions import InvalidInput, InvalidUserCode
from log_record_manager import LogManager
import logging
logging.basicConfig(filename="logs.log", level= logging.DEBUG)

# User String Format:
# "username | user_code | user_id"
# Designed for use with rc522 module, wired as required by the mfrc522 module


class LoginManager:

    security_manager: SecurityManager
    reader: Reader
    presenter: Presenter
    user_log_manager: LogManager
    user_manager: UserManager

    def __init__(self, reader: Reader,
                 presenter: Presenter = SimplePresenter()):
        """Creates a new LoginManager with a certain presenter strategy"""
        self.security_manager = SecurityManager()
        self.reader = reader
        self.presenter = presenter
        self.user_log_manager = LogManager()
        self.user_manager = UserManager(presenter, self.reader,
                                        self.security_manager,
                                        self.user_log_manager)

    def run_login_system(self) -> int:
        """Runs the loginsystem system"""
        self.user_manager.register_new_user()
        # Main loop
        # Fetch any data available from the RFID reader
        data = self.reader.get_tag_data()
        valid_user = self.check_for_user(data)
        if valid_user:
            self.run_sign_in_process(valid_user)

        return valid_user.get_id()


    def add_new_user(self):
        """Adds a new user to the directory"""


    def run_login(self):
        """Runs the loginsystem system once"""

    def check_for_user(self, input_data: str) -> bool or User:
        """Checks if the data is a valid users' data. Shows corresponding error
        messages iff the user's data isn't formatted properly."""
        try:
            user = self.user_manager.user_from_input(input_data)
            return user
        except InvalidInput:
            logging.exception(InvalidInput)
            self.presenter.print("Bad Read or Invalid Key")
        except InvalidUserCode:
            logging.exception(InvalidUserCode)
            self.presenter.print("User code invalid")
        return False

    def run_sign_in_process(self, user: User):
        """Runs the series of events that should occur when a user taps onto the
        reader."""
        self.presenter.print(self.user_log_manager.get_login_str(user))
        self.user_log_manager.add_tap_log(user)
