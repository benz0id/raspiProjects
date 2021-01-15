from Presenters import LCD
from Reader import Reader
from LoginManager import LoginManager
from time import sleep
import threading



reader = Reader()
lcd = LCD()
login_manager = LoginManager(reader, lcd)

rfid_login = threading.Thread(target=login_manager.run_login_system())

rfid_login.start()
