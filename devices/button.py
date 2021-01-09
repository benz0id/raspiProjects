from .device import Device
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)


class Button(Device):

    def is_running(self) -> bool:
        pass

    _pin: int
    _running: bool

    def __init__(self, pin: int):
        """Initialises a new button and configures its pin as an output."""
        GPIO.setup(pin, GPIO.IN)
        self.pin = pin

    def state(self):
        """Gets the state of the button"""
        return GPIO.

