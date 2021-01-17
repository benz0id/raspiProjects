import RPi.GPIO as GPIO
from .led import Led
from threading import Thread
import logging

GPIO.setmode(GPIO.BCM)


def triple_blink(led: Led):
    """Blinks <led> three times if it isn't running."""
    if not led.is_running():
        thread = Thread(target=led.blink, args=(3, 0.3, 0.3))
        thread.start()
    else:
        logging.debug("Could not flash LED, was running")


class LedManager:
    _red_led: Led
    _green_led: Led

    def __init__(self, red_led_pin: int, green_led_pin: int):
        """Initialises a new led manager with the specified LEDs"""
        self._red_led = Led(red_led_pin)
        self._green_led = Led(green_led_pin)

    def unlocked_display(self):
        """Blinks the green led three times"""
        logging.info("Flashing Green LED")
        triple_blink(self._green_led)

    def locked_display(self):
        """Blinks the red led three times"""
        logging.info("Flashing Red LED")
        triple_blink(self._red_led)

    def strobe(self, led: int = 0):
        """Strobes an LED"""
        if led:
            led = Led(led)

        led = self._red_led
        led.blink(50, 0.01, 0.01)




