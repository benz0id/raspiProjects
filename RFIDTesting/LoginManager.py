from datetime import datetime
from typing import Tuple
from Reader import Reader
from Presenters import SimplePresenter, Presenter
from SecurityManager import SecurityManager
from UserManager import UserManager
from User import User
from Exceptions import InvalidInput, InvalidUserCode
from LogManager import LogManager
from time import sleep
import logging
logging.basicConfig(filename='logs.log', level=logging.DEBUG)

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

    def run_login_system(self):
        """Runs the login system continually"""
        self.user_manager.register_new_user()
        # Main loop
        while True:
            # Fetch any data available from the RFID reader
            data = self.reader.get_tag_data()

            # Handle the data received
            self.handle_received_data(data)

            # Wait two seconds
            sleep(2)

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

    def handle_received_data(self, input_data: str):
        """Handles the process that occurs after user data is received."""
        valid_user = self.check_for_user(input_data)
        if valid_user:
            self.run_sign_in_process(valid_user)

    def run_sign_in_process(self, user: User):
        """Runs the series of events that should occur when a user taps onto the
        reader."""
        self.presenter.print(self.user_log_manager.get_login_str(user))
        self.user_log_manager.add_tap_log(user)
