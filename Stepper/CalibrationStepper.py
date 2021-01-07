from time import sleep
import RPi.GPIO as GPIO
import logging
from typing import List
from math import pi
from datetime import datetime
from math import ceil


logging.basicConfig(filename="logs.log", level=logging.DEBUG)

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# A half step sequence for the 28BYJ-28 stepper motor
SEQ_HALF_28BYJ_28 = [[1, 0, 0, 1],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

# A full step sequence for the 28BYJ-28 stepper motor
SEQ_FULL_28BYJ_28 = [[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]


def delay(milliseconds: float):
    """Sleeps for <milliseconds>"""
    sleep(milliseconds / 1000)


class CalibrationStepper:
    """A stepper motor driver."""

    # === Private Attributes ===
    # _step_pins:
    #       The pins that should be written to in order to drive the stepper.
    # _num_pins:
    #       The number of pins in the stepper.
    # _steps:
    #       The number of steps in a full rotation of the motor.
    # _seq:
    #       The sequence of steps taken to progress the motor, can be half or
    #       full step.
    # _mode:
    #       Indicates whether the motor is in half or full step mode.
    #       0 -> full step
    #       1 -> half step
    #
    # === Representation Invariants ===
    # For all n len(_seq[n]) == len(num_pins)

    _step_pins: List[int]
    _steps: int
    _num_pins: int
    _seq: List[List[int]]
    _mode: int
    half_steps_completed: int

    def __init__(self, step_pins: List[int], steps: int, seq: List[List[int]],
                 mode: int = 1):
        """Initialises a new stepper motor"""
        self._step_pins = step_pins
        self._steps = steps
        self._mode = mode
        self._num_pins = len(step_pins)
        self._seq = seq
        self.half_steps_completed = 0
        logging.info("Setting up stepper pins as output")
        for pin in step_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def turn(self, direction: int, speed: float, radians: float):
        """Turns the stepper motor <radians> degrees at a rate of <speed>
        radians per second. Turns clockwise iff <direction> is 1 else turns
        counterclockwise"""
        start = datetime.now()
        delay_time = self.speed_to_milliseconds(speed)
        print("Calculated delay time for each " + [
            "full step: ", "half step: "][self._mode] + str(delay_time))
        rads_per_stp_cyc = 2 * pi / self._steps * len(self._seq) \
                                  / (1 + self._mode)
        print("Calculated radians per step cycle" + str(rads_per_stp_cyc))
        stp_cycles = ceil(radians / rads_per_stp_cyc)
        print("Calculated step cycles:" + str(stp_cycles))
        for _ in range(stp_cycles):
            print("Step cycle #" + str(_))
            self.one_step_cycle(direction, delay_time)
        self.disengage()
        print(["full steps ", "half steps "][self._mode] + "completed: " +
              str(self.half_steps_completed))
        print("Runtime: " + str(datetime.now() - start))
        print("Target runtime: " + str(self.half_steps_completed * delay_time
                                       / 1000))
        print("Goal runtime: " + str(radians / speed))
        self.half_steps_completed = 0

    def one_step_cycle(self, direction: int, delay_time: float):
        """Turns the motor one step sequence in the specified direction, waiting
        delay time milliseconds between each step"""
        for step in self._seq[::direction]:
            for i in range(self._num_pins):
                GPIO.output(self._step_pins[i], step[i])
            self.half_steps_completed += 1
            delay(delay_time)

    def speed_to_milliseconds(self, speed: float) -> float:
        """Returns the delay time (in milliseconds) between each step/half step
        required to achieve the desired <speed>"""
        rad_per_step = 2 * pi / self._steps / (1 + self._mode)
        step_per_second = rad_per_step / speed
        # Converting to milliseconds and accounting for step mode
        return step_per_second * 1000

    def disengage(self):
        """Disengages the motor."""
        for pin in self._step_pins:
            GPIO.output(pin, 0)
