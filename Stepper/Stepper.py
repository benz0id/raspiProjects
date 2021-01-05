#!/usr/bin/python
# Import required libraries
# https://www.raspberrypi-spy.co.uk/2012/07/stepper-motor-control-in-python/
import sys
import time
import RPi.GPIO as GPIO
import logging
logging.basicConfig(filename="logs.log", level= logging.DEBUG)

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
StepPins = [19, 26, 16, 20]

# Set all pins as output
for pin in StepPins:
    logging.info("Setup pins")
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1, 0, 0, 1],
       [1, 0, 0, 0],
       [1, 1, 0, 0],
       [0, 1, 0, 0],
       [0, 1, 1, 0],
       [0, 0, 1, 0],
       [0, 0, 1, 1],
       [0, 0, 0, 1]]

StepCount = len(Seq)
StepDir = 1  # Set to 1 or 2 for clockwise
# Set to -1 or -2 for anti-clockwise

# Read wait time from command line
WaitTime = float(1)

# Initialise variables
StepCounter = 0

# Start main loop
while True:

    logging.info(StepCounter)
    logging.info(Seq[StepCounter])

    for pin in range(0, 4):
        xpin = StepPins[pin]  #
        if Seq[StepCounter][pin] != 0:
            logging.info(" Enable GPIO %i" % xpin)
            GPIO.output(xpin, True)
        else:
            GPIO.output(xpin, False)

    StepCounter += StepDir

    # If we reach the end of the sequence
    # start again
    if StepCounter >= StepCount:
        StepCounter = 0
    if StepCounter < 0:
        StepCounter = StepCount + StepDir

    # Wait before moving on
    time.sleep(WaitTime)
