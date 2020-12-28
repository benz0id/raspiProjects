import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
from User import User

reader = SimpleMFRC522()
GPIO.setwarnings(False)


class Reader:
    reader = SimpleMFRC522()

    def write(self, string: str):
        """Writes a given string to the tag"""
        try:
            reader.write(string)
        finally:
            GPIO.cleanup()

    def get_tag_data(self) -> str:
        """Interprets and returns the data stored in the tag.
        #TODO add encryption to this function"""
        return self.read_data()

    def read_data(self) -> str:
        """Reads the data input from the RFID"""
        try:
            tag_id, user_info = reader.read()
        finally:
            GPIO.cleanup()
        # TODO add a logger for all tag_ids added
        return user_info

    def write_user_to_tag(self, user: User):
        """Writes new user info to an RFID tag. Waits for a tag to contact.
        Written info format:
        'entered_username|last_login_datetime('%Y-%m-%d %H:%M:%S')' """
        user_info = ""
        attributes = [
            user.get_username(),
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            user.get_key()
        ]

        for attribute in attributes:
            user_info += attribute
            user_info += "|"

        user_info = user_info[0:-1]

        try:
            reader.write((user_info))
        finally:
            GPIO.cleanup()
