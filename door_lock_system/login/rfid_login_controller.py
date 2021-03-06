from datetime import datetime, timedelta
from threading import Thread
from typing import List

from design_patterns.observer import Observer, Subject
from devices.led_manager import LedManager
from .log_record_manager import LogManager
from devices.presenters import ConsolePresenter, Presenter
from devices.reader import Reader
from .security_manager import SecurityManager
from .user_manager import UserManager

# The delay between logins
LOGIN_DELAY = 30


class RFIDLoginController(Subject):
    _security_manager: SecurityManager
    _reader: Reader
    _presenter: Presenter
    _user_log_manager: LogManager
    _user_manager: UserManager
    _led_manager: LedManager

    _observers: List[Observer] = []

    _last_sign_in_id: int
    _last_sign_in: datetime

    _run_rfid_scanner: bool

    def __init__(self, reader: Reader,
                 led_manager: LedManager,
                 presenter: Presenter = ConsolePresenter()):
        """Creates a new LoginManager with a certain presenter strategy"""
        self._security_manager = SecurityManager()
        self._reader = reader
        self._presenter = presenter
        self._user_log_manager = LogManager()
        self._led_manager = led_manager
        self._user_manager = UserManager(presenter, self._reader,
                                         self._security_manager,
                                         self._user_log_manager)
        self._last_sign_in_id = -1
        self._last_sign_in = datetime(2000, 2, 2, 2, 2, 2)
        self._run_rfid_scanner = True

    def run_rfid_scanner(self):
        """Runs the RFID scanner while self._run_rfid_scanner in a separate
        thread"""
        rfid_thread = Thread(target=self.run_login_system)
        rfid_thread.start()

    def run_login_system(self):
        """Runs the login system system, returns a userID if found"""
        while self._run_rfid_scanner:
            # Main loop
            # Fetch any data available from the RFID reader
            data = self._reader.get_tag_data()
            succesful_login = self._user_manager.check_for_user(data)
            if succesful_login and self._user_manager.logged_in_cleared():
                self.run_timed_processes()
                self.notify()
            elif self._user_manager.logged_in_cleared():
                self.run_timed_processes()
                self._presenter.print("User not cleared for access."
                                      " Contact the admin")
            else:
                self._led_manager.strobe()


    def add_new_user(self):
        """Adds a new user to the directory"""
        self.run_timed_processes()
        self._user_manager.register_new_user()

    def run_timed_processes(self):
        """Runs the series of events that should occur when a user taps onto the
        reader."""
        if not(self.get_cur_user_id() == self._last_sign_in_id and
                datetime.now() - self._last_sign_in <
                timedelta(0, LOGIN_DELAY)):
            # Update sign in id
            self._last_sign_in_id = self.get_cur_user_id()
            self._last_sign_in = datetime.now()
            # Display the login string
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
