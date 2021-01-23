import logging

import RPi.GPIO as GPIO

from devices.device_controller import DeviceController
from devices.lock import Lock
from devices.misc_info import GREEN_LED_PIN, LOCK_DIRECTION, LOCK_TURNS, \
    RED_LED_PIN, STEPPER_PINS, STEPPER_SPEED
from devices.presenters import LCD
from devices.reader import Reader
from devices.stepper import NUM_STEPS_28BYJ_28, SEQ_HALF_28BYJ_28, Stepper
from devices.led_manager import LedManager

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
logging.basicConfig(filename="logs.log", level=logging.DEBUG)

stepper_motor = Stepper(STEPPER_PINS,
                        NUM_STEPS_28BYJ_28,
                        SEQ_HALF_28BYJ_28)
presenter = LCD()
rfid_reader = Reader()

lock = Lock(stepper_motor, LOCK_DIRECTION, LOCK_TURNS, STEPPER_SPEED)
led_m = LedManager(RED_LED_PIN, GREEN_LED_PIN)
devices = DeviceController(lock, rfid_reader, presenter, led_m)

devices.lock()
