from login.user_manager import UserManager
from devices.presenters import ConsolePresenter
from devices.reader import Reader
from login.security_manager import SecurityManager
from login.log_record_manager import LogManager
import RPi.GPIO as GPIO

presenter = ConsolePresenter()

um = UserManager(presenter, Reader(), SecurityManager(), LogManager())

num_logins = presenter.input("Enter the number of past "
                                 "logins you would like to see.")

while not num_logins.isnumeric():

    presenter.print("Invalid input. moron.")

    num_logins = presenter.input("Enter the number of past "
                                 "logins you would like to see.")

presenter.print(um.view_recent_logins(int(num_logins)))

GPIO.cleanup()


