from login.user_manager import UserManager
from devices.presenters import ConsolePresenter
from devices.reader import Reader
from login.security_manager import SecurityManager
from login.log_record_manager import LogManager

um = UserManager(ConsolePresenter(), Reader(), SecurityManager(), LogManager())

um.register_new_user()


