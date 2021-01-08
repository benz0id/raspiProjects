# The GPIO pins

# The reader pins are defined in the SimpleMFRC522 module as show below
#     SDA connects to Pin 24.
#     SCK connects to Pin 23.
#     MOSI connects to Pin 19.
#     MISO connects to Pin 21.
#     GND connects to Pin 6.
#     RST connects to Pin 22.
#     3.3v connects to Pin 1.
READER_PINS = None

# The LCD's pins are configured using generic GPIOs 2 & 3 using standard I2C
# protocol.
LCD_PINS = None

# The stepper driver pins.
# Other custom stepper info can be added in stepper
STEPPER_PINS = [19, 26, 16, 20]

# The lock locks by moving in this direction (when looking up the shaft,
# 0 -> counter clockwise, 1 -> clockwise).
LOCK_DIRECTION = 1

# The number of stepper turns required to unlock/unlock the lock
LOCK_TURNS = 0.5

# The speed at which the stepper should rotate
STEPPER_SPEED = 0.25


