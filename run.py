import logging

import RPi.GPIO as GPIO

from device_controller import DeviceController
from lock import Lock
from login.rfid_login_controller import RFIDLoginController
from misc_info import LOCK_DIRECTION, LOCK_TURNS, STEPPER_PINS
from presenters import LCD
from reader import Reader
from devices.stepper import NUM_STEPS_28BYJ_28, SEQ_HALF_28BYJ_28, Stepper

GPIO.setmode(GPIO.BCM)
logging.basicConfig(filename="logs.log", level=logging.DEBUG)

stepper_motor = Stepper(STEPPER_PINS,
                                NUM_STEPS_28BYJ_28,
                                SEQ_HALF_28BYJ_28)
presenter = LCD()
rfid_reader = Reader()

lock = Lock(stepper_motor, LOCK_DIRECTION, LOCK_TURNS)

rfid_controller = RFIDLoginController(rfid_reader, presenter)
devices = DeviceController(lock, rfid_reader, presenter)

rfid_controller.attach(devices)

rfid_controller.run_rfid_scanner()
