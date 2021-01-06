from CalibrationStepper import CalibrationStepper, SEQ_28BYJ_28
from math import pi

step_pins = [19, 26, 16, 20]
stepper = CalibrationStepper(step_pins, 2000, SEQ_28BYJ_28)
print("Turning the stepper")
stepper.turn(1, 0.25, 2 * pi)
