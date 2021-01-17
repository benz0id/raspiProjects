from threading import Thread
from typing import List

import logging

from design_patterns.observer import Observer
from .device import Device
from .stepper import Stepper


class Lock(Device):
    """A door lock.
    === Private Attributes ===
    _stepper:
            The stepper used to lock and unlock.
    _is_locked:
            The lock's status.
    _rotations_to_lock:
            The number of rotations of the stepper needed to unlock/lock.
    _lock_direction:
            The direction in which the stepper rotates to lock the door.
    _stepper_speed:
            The speed with which the lock closes.
    _observers:
            All observers that should be notified when this lock is
            opened/closed.
    """

    _stepper: Stepper
    _rotations_to_lock: float
    _lock_direction: int
    _stepper_speed: float

    _is_running: bool
    _stepper_thread: Thread

    _is_locked: bool
    _observers: List[Observer]

    def __init__(self, stepper: Stepper, lock_direction: int,
                 rotations_to_lock: float, stepper_speed: int):
        """Initialises a new lock that uses <stepper> to lock, which is done in
         <lock_direction>, by turning <rotation_to_lock> times at
         <stepper_speed> turns per second"""
        super()
        self._stepper = stepper
        self._rotations_to_unlock = rotations_to_lock
        self._lock_direction = lock_direction
        self._stepper_speed = stepper_speed
        self._observers = []
        self._is_locked = False
        self._is_running = False

    def lock(self):
        """Locks the lock."""
        logging.info("Locking the lock")
        self._stepper_thread = Thread(target=self.lock_stepper)
        self._stepper_thread.start()
        self._is_locked = True

    def lock_stepper(self):
        """Causes the stepper to lock the lock"""
        self._is_running = True
        self._stepper.turn(
            self._lock_direction,
            self._stepper_speed,
            self._rotations_to_unlock)
        self._is_running = False

    def unlock(self):
        """Unlocks the lock."""
        logging.info("Unlocking the lock")
        self._stepper_thread = Thread(target=self.unlock_stepper)
        self._stepper_thread.start()
        self._is_locked = False

    def unlock_stepper(self):
        """Causes the stepper to unlock the lock"""
        self._is_running = True
        self._stepper.turn(
            self._lock_direction - 1,
            self._stepper_speed,
            self._rotations_to_unlock)
        self._is_running = False

    def set_status(self, is_locked: bool):
        """Sets the locks state."""
        self._is_locked = is_locked

    def is_locked(self) -> bool:
        """Returns whether the lock is locked. Locked iff true"""
        return self._is_locked

    def is_running(self) -> bool:
        """Returns whether this lock is running."""
        return self._is_running





