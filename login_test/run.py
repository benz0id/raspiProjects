from presenters import LCD
from reader import Reader
from login_manager import LoginManager
from time import sleep
import threading


reader = Reader()
lcd = LCD()
login_manager = LoginManager(reader, lcd)

login_manager.user_manager.register_new_user()

rfid_login = threading.Thread(target=login_manager.run_login_system)

rfid_login.start()
