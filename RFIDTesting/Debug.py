from datetime import datetime
from Presenter import SimplePresenter
from UserManager import UserManager
from SecurityManager import SecurityManager
presenter = SimplePresenter()
security_manager = SecurityManager()
reader = 1
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

def handle_received_data(data: str):
    """Handles the process that occurs after user data is received."""
    valid_user, user = check_for_user(data)
    if valid_user:
        presenter.print(user.get_login_str())
        try:
            reader.write_user_to_tag(user)
        finally:
            GPIO.cleanup()

handle_received_data("Kyle" + "|" +
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "|" +
                     str(119218851371))
