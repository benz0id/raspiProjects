from CalibrationStepper import CalibrationStepper, SEQ_FULL_28BYJ_28, \
    SEQ_HALF_28BYJ_28
from Stepper import Stepper
from math import pi

seq = SEQ_HALF_28BYJ_28
mode = 1

step_pins = [19, 26, 16, 20]
stepper = CalibrationStepper(step_pins, 2048, seq, mode)
stepper1 = Stepper(step_pins, 2048, seq, mode)
print("Turning the cstepper")
stepper.turn(1, pi / 2, 2 * pi, simple_half_step=True)
print("Turning the stepper")
stepper1.turn(1, pi / 2, 30 * 2 * pi, simple_half_step=True)
