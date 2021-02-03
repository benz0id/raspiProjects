from calibration_stepper import CalibrationStepper, SEQ_HALF_28BYJ_28
from stepper import Stepper

seq = SEQ_HALF_28BYJ_28
mode = 1

step_pins = [19, 26, 16, 20]
stepper = Stepper(step_pins, 2048, seq, mode)
stepper1 = Stepper(step_pins, 2048, seq, mode)
print("Turning the cstepper")
stepper.turn(0, 0.25, 0.5)
print("Turning the stepper")
stepper1.turn(1, 0.25, 0.5)
