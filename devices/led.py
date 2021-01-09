from .device import Device
import RPi.GPIO as GPIO
from time import sleep
import logging

GPIO.setmode(GPIO.BCM)


class Led(Device):

    _pin: int
    _running: bool

    def __init__(self, pin: int):
        """Initialises a new led and configures its pin as an output."""
        GPIO.setup(pin, GPIO.OUT)
        self._pin = pin
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def blink(self, num_blinks: int, on_time: float, off_time: float):
        """Blinks the led <num_blinks> times, with it being on for <on_time> and
        off for <off_time>."""
        self._running = True
        logging.info("Flashing LED at pin:" + str(self._pin))
        for _ in range(num_blinks):
            GPIO.output(self._pin, 1)
            sleep(on_time)
            GPIO.output(self._pin, 0)
            sleep(off_time)
        self._running = False




