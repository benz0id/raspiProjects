from datetime import datetime
from typing import Tuple
from Reader import Reader
from Presenters import SimplePresenter
from SecurityManager import SecurityManager
from UserManager import UserManager
from User import User
from UserManager import InvalidInput, InvalidUserCode
from LogManager import LogManager
from time import sleep

# User String Format:
# "username | user_code | user"
# Designed for use with rc522 module, wired as required by the mfrc522 module

security_manager = SecurityManager()
reader = Reader()
presenter = SimplePresenter()
user_log_manager = LogManager()
user_manager = UserManager(presenter, reader, security_manager, user_log_manager)


def check_for_user(input_data: str) -> bool or User:
    """Checks if the data is a valid users' data. Shows corresponding error
    messages iff the user's data isn't formatted properly."""
    try:
        user = user_manager.user_from_input(input_data)
        return user
    except InvalidInput:
        presenter.print("Bad Read or Invalid Key")
    except InvalidUserCode:
        presenter.print("User code invalid")
    return False


def handle_received_data(input_data: str):
    """Handles the process that occurs after user data is received."""
    valid_user = check_for_user(input_data)
    if valid_user:
        run_sign_in_process(valid_user)


def run_sign_in_process(user: User):
    """Runs the series of events that should occur when a user taps onto the
    reader."""
    presenter.print(user_log_manager.get_login_str(user))
    user_log_manager.add_tap_log(user)


# Main loop
while True:
    data = reader.get_tag_data()
    handle_received_data(data)
    sleep(0.5)
