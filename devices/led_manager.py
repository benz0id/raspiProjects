import RPi.GPIO as GPIO
from .led import Led
from threading import Thread
import logging

GPIO.setmode(GPIO.BCM)


class LedManager:
    _red_led: Led
    _green_led: Led

    def __init__(self, red_led_pin: int, green_led_pin: int):
        """Initialises a new led manager with the specified LEDs"""
        self._red_led = Led(red_led_pin)
        self._green_led = Led(green_led_pin)

    def unlocked_display(self):
        """Blinks the green led three times"""
        self.triple_blink(self._green_led)
        logging.info("Flashing Green LED")

    def locked_display(self):
        """Blinks the red led three times"""
        self.triple_blink(self._red_led)
        logging.info("Flashing Red LED")

    def triple_blink(self, led: Led):
        """Blinks <led> three times if it isn't running."""
        if not led.is_running():
            thread = Thread(target=self._red_led.blink(3, 0.3, 0.3))
            thread.start()


