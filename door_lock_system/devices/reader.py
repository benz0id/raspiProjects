import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522
import logging
from time import sleep

GPIO.setwarnings(False)


# Encryption removed as encrypted string is too long to be stored in standard
# RFID tag, may be re-implemented if more efficient algorithm is found

class Reader:
    """Adapts the SimpleMFRC522 reader"""

    reader_fxns = MFRC522()
    reader = SimpleMFRC522()

    def write(self, string: str):
        """Writes a given string to the tag"""
        self.reader.write(string)

    def get_tag_data(self) -> str:
        """Interprets and returns the data stored in the tag.
        # TODO add encryption to this function"""
        return self.read_data()

    def read_data(self) -> str:
        """Reads the data input from the RFID"""
        user_info = ""
        tag_id = 0
        while not user_info:
            try:
                tag_id, user_info = self.reader.read_no_block()
                self.reader_fxns.MFRC522_Reset()
                sleep(0.2)
            except KeyboardInterrupt:
                logging.exception("Keyboard Interrupt!")
            # print(tag_id, user_info)

        # print("hit!")

        return user_info
