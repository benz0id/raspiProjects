from door_lock_system.login import UserManager
from door_lock_system.devices import ConsolePresenter
from door_lock_system.devices import Reader
from door_lock_system.login import SecurityManager
from door_lock_system.login import LogManager
import RPi.GPIO as GPIO

um = UserManager(ConsolePresenter(), Reader(), SecurityManager(), LogManager())

um.register_new_user()

GPIO.cleanup()


