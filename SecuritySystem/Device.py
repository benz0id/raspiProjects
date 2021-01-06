import RPi.GPIO as GPIO

"""A security device"""
class Device:

    pin: int
    name: str

    # True -> Normally High
    # False -> Normally Low
    default_state: bool

    def __init__(self, pin: int, name: str, default_state: bool):
        self.pin = pin
        self.name = name
        self.default_state = default_state





