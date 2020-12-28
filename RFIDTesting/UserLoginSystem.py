from datetime import datetime
import RPi.GPIO as GPIO
from typing import Tuple, List
from Reader import Reader
from Presenter import SimplePresenter
from SecurityManager import SecurityManager
from UserManager import UserManager
from User import User
from UserManager import InvalidInput, InvalidUserCode

# User String Format:
# username:str | lastlogin
# Designed for use with rc522 module, wired as required by the mfrc522 module

security_manager = SecurityManager()
reader = Reader()
presenter = SimplePresenter()
user_manager = UserManager(presenter, reader, security_manager)

def check_for_user(data: str) -> Tuple[bool, User]:
    """Checks if the data is a valid users' data. Shows corresponding error
    messages iff the user's data isn't formatted properly."""
    try:
        user = user_manager.user_from_input(data)
        return True, user
    except InvalidInput:
        presenter.print("Bad Read")
    except InvalidUserCode:
        presenter.print("User is no longer cleared for access")

    return False, User("", datetime.now(), 0)


def handle_received_data(data: str):
    """Handles the process that occurs after user data is received."""
    valid_user, user = check_for_user(data)
    if valid_user:
        presenter.print(user.get_login_str())
        try:
            reader.write_user_to_tag(user)
        finally:
            GPIO.cleanup()


# Main loop
while True:
    try:
        data = reader.get_tag_data()
        handle_received_data(data)

    finally:
        GPIO.cleanup()
