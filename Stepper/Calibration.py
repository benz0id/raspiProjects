from CalibrationStepper import CalibrationStepper, SEQ_FULL_28BYJ_28
from Stepper import Stepper
from math import pi

step_pins = [19, 26, 16, 20]
stepper = CalibrationStepper(step_pins, 2048, SEQ_FULL_28BYJ_28)
stepper1 = Stepper(step_pins, 2048, SEQ_FULL_28BYJ_28)
print("Turning the cstepper")
stepper.turn(1, pi / 2, 2 * pi)
print("Turning the stepper")
stepper1.turn(1, pi / 2, 2 * pi)
