import RPi.GPIO as GPIO
from devices.lock import Lock
from devices.misc_info import LOCK_DIRECTION, LOCK_TURNS, STEPPER_PINS, \
    STEPPER_SPEED
from devices.stepper import NUM_STEPS_28BYJ_28, SEQ_HALF_28BYJ_28, Stepper

GPIO.setmode(GPIO.BCM)

stepper_motor = Stepper(STEPPER_PINS,
                        NUM_STEPS_28BYJ_28,
                        SEQ_HALF_28BYJ_28)

lock = Lock(stepper_motor, LOCK_DIRECTION, LOCK_TURNS, STEPPER_SPEED)

lock.lock()
