from lock import Lock
from reader import Reader
from stepper import Stepper
from presenters import Presenter
from security_device import SecurityDevice
from typing import List
from DPs.observer import Observer, Subject


class DeviceController(Observer):
    """Manages all IO controlled devices used by this program. Devices are
    treated like entities.

    Observer: observes the LoginController, changes lock state when valid login
    is received.

    === Private Attributes ===
    _lock:
            A lock used to open and close a door
    _reader:
            A device used to read data from a RFID tag.
    _presenter:
            A presenter used to show information to the user
    _security_devices:
            Devices that monitor activity.
    """
    _lock: Lock
    _reader: Reader
    _presenter: Presenter
    _security_devices: List[SecurityDevice]

    def __init__(self, lock: Lock, reader: Reader, presenter: Presenter):
        """Initialises a new manager."""
        self._lock = lock
        self._reader = reader
        self._presenter = presenter
        self._security_devices = []

    def add_security_device(self, device: SecurityDevice):
        """Adds a security device to the list of security devices"""
        self._security_devices.append(device)

    def lock(self):
        """Locks the lock"""
        if not self._lock.is_running():
            self._lock.lock()

    def unlock(self):
        """Unlocks the lock"""
        if not self._lock.is_running():
            self._lock.unlock()

    def lock_is_locked(self) -> bool:
        """Gets the state of the lock, locked iff True."""
        return self._lock.is_locked()

    def set_lock_state(self, state: bool):
        """Sets the state of the lock."""
        self.set_lock_state(state)

    def switch_lock_state(self):
        """Switches the lock to its other state."""
        if self._lock.is_running():
            pass
        elif self.lock_is_locked():
            self.lock()
        else:
            self.unlock()

    def get_presenter(self):
        """Gets the presenter."""
        return self._presenter

    def get_reader(self):
        """Gets the reader."""
        return self._reader

    def update(self, subject: Subject) -> None:
        """Switches lock state.
        # TODO add user-specific features"""
        self.switch_lock_state()




