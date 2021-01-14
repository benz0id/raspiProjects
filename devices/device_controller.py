from typing import List

from design_patterns.observer import Observer, Subject
from .lock import Lock
from .presenters import Presenter
from .reader import Reader
from .security_device import SecurityDevice
from .led_manager import LedManager
import RPi.GPIO as GPIO
from time import sleep


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
    _led_manager:
            A manager that operates attached LEDS.
    """
    _lock: Lock
    _reader: Reader
    _presenter: Presenter
    _security_devices: List[SecurityDevice]
    _led_manager: LedManager

    def __init__(self, lock: Lock, reader: Reader, presenter: Presenter,
                 led_manager: LedManager):
        """Initialises a new manager."""
        self._lock = lock
        self._reader = reader
        self._presenter = presenter
        self._security_devices = []
        self._led_manager = led_manager

    def add_security_device(self, device: SecurityDevice):
        """Adds a security device to the list of security devices"""
        self._security_devices.append(device)

    def lock(self):
        """Locks the lock"""
        if not self._lock.is_running():
            self._lock.lock()
            self._led_manager.locked_display()

    def unlock(self):
        """Unlocks the lock"""
        if not self._lock.is_running():
            self._lock.unlock()
            self._led_manager.unlocked_display()

    def lock_is_locked(self) -> bool:
        """Gets the state of the lock, locked iff True."""
        return self._lock.is_locked()

    def set_lock_state(self, state: bool):
        """Sets the state of the lock."""
        self.set_lock_state(state)

    def switch_lock_state(self, callable=None):
        """Switches the lock to its other state."""
        if self._lock.is_running():
            pass
        elif self.lock_is_locked():
            self.unlock()
        else:
            self.lock()

    def add_lock_button(self, button_pin: int):
        """Add as a switch that regulates the lock. Opens lock when the button
        rises.
        ###### Interferes with other processes ######"""
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button_pin, GPIO.RISING,
                              callback=self.poll_lock_button)

    def poll_lock_button(self, button_pin):
        """Constantly polls a button, switches the lock state if pressed"""
        prev_input = 0
        while True:
            input = GPIO.input(button_pin)
            if (not prev_input) and input:
                self.switch_lock_state()
            prev_input = input
            sleep(0.05)

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




