from devices.device import Device
from devices.stepper import Stepper


class Lock(Device):
    """A door lock.
    === Private Attributes ===
    _stepper:
            The stepper used to lock and unlock.
    _is_locked:
            The lock's status.
    _rotations_to_unlock:
            The number of rotations of the stepper needed to unlock/lock.
    """

    _stepper: Stepper
    _is_locked: bool
    _rotations_to_unlock: float

    def __init__(self, stepper: Stepper, rotations_to_lock: float):
        """Initialises a new lock that uses <stepper> to lock and unlock.
         <rotations_to_unlock> specifies the number of rotations of the stepper
         needed to unlock the door"""
        super()
        self._stepper = stepper
        self._rotations_to_unlock = rotations_to_lock






