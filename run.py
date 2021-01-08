import logging

from devices import device_controller, lock, misc_info, presenters, reader, \
    stepper
from login.rfid_login_controller import RFIDLoginController

logging.basicConfig(filename="logs.log", level=logging.DEBUG)

stepper_motor = Stepper(misc_info.STEPPER_PINS, stepper.NUM_STEPS_28BYJ_28,
                                stepper.SEQ_HALF_28BYJ_28)
presenter = LCD()
rfid_reader = reader.Reader()

lock = lock.Lock(stepper_motor, misc_info.LOCK_DIRECTION, misc_info.LOCK_TURNS)

rfid_controller = RFIDLoginController(rfid_reader, presenter)
devices = device_controller.DeviceController(lock, rfid_reader, presenter)

rfid_controller.attach(devices)

rfid_controller.run_rfid_scanner()
