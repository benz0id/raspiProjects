from LogManager import LogManager
from User import User


log_manager = LogManager()

log_manager.register_new_user(User["Jared", 13, 0])
user = log_manager.get_user(0)

print(user.get_username())
