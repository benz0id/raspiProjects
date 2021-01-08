from datetime import datetime, timedelta
from threading import Thread
from typing import List

from design_patterns.observer import Observer, Subject
from log_record_manager import LogManager
from presenters import ConsolePresenter, Presenter
from reader import Reader
from security_manager import SecurityManager
from user_manager import UserManager

# The delay between logins
LOGIN_DELAY = 30


class RFIDLoginController(Subject):
    _security_manager: SecurityManager
    _reader: Reader
    _presenter: Presenter
    _user_log_manager: LogManager
    _user_manager: UserManager

    _observers: List[Observer] = []

    _last_sign_in_id: int
    _last_sign_in: datetime

    _run_rfid_scanner: bool

    def __init__(self, reader: Reader,
                 presenter: Presenter = ConsolePresenter()):
        """Creates a new LoginManager with a certain presenter strategy"""
        self._security_manager = SecurityManager()
        self._reader = reader
        self._presenter = presenter
        self._user_log_manager = LogManager()
        self._user_manager = UserManager(presenter, self._reader,
                                         self._security_manager,
                                         self._user_log_manager)
        self._last_sign_in_id = -1
        self._last_sign_in = datetime.now() - datetime(2000, 2, 2, 2, 2, 2)
        self._run_rfid_scanner = True

    def run_rfid_scanner(self):
        """Runs the RFID scanner while self._run_rfid_scanner in a separate
        thread"""
        rfid_thread = Thread(target=self.run_login_system())
        rfid_thread.start()

    def run_login_system(self):
        """Runs the login system system, returns a userID if found"""
        while self._run_rfid_scanner:
            # Main loop
            # Fetch any data available from the RFID reader
            data = self._reader.get_tag_data()
            succesful_login = self._user_manager.check_for_user(data)
            if succesful_login:
                self.notify()

    def add_new_user(self):
        """Adds a new user to the directory"""
        self._user_manager.register_new_user()

    def timed_processes(self):
        """Runs the series of events that should occur when a user taps onto the
        reader."""
        if not (self.get_cur_user_id() == self._last_sign_in_id and
                datetime.now() - self._last_sign_in >
                timedelta(0, LOGIN_DELAY)):
            self._presenter.print(self.get_cur_login_str())
            self._user_log_manager.add_tap_log(self.get_cur_user_id())

    def get_cur_user_id(self) -> int:
        """Gets the most recently logged in user's id"""
        return self._user_manager.get_cur_user_id()

    def get_cur_login_str(self) -> str:
        """Returns the most recently logged in user's login str"""
        return self._user_manager.get_cur_login_str()

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)
