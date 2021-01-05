import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
from User import User
from cryptography.fernet import Fernet, InvalidToken
import os.path
import logging

GPIO.setwarnings(False)
# Encryption removed as encrypted string is too long to be stored in standard
# RFID tag, may be re-implemented if more efficient algorithm is found
"""
# Load key from file if it already exists, otherwise create a file and key
key_file_path = os.path.join("Users", "Key.txt")

try:
    key_file = open(key_file_path, "rb")
    key = bytes(key_file.readlines()[0])
    key_file.close()
except FileNotFoundError:
    key_file = open(key_file_path, "wb")
    key = Fernet.generate_key()
    key_file.write(key)
    key_file.close()

f = Fernet(key)
"""


class Reader:
    """Adapts the SimpleMFRC522 reader"""
    reader = SimpleMFRC522()

    def write(self, string: str):
        """Writes a given string to the tag"""
        try:
            self.reader.write(string)
        finally:
            GPIO.cleanup()

    def get_tag_data(self) -> str:
        """Interprets and returns the data stored in the tag.
        #TODO add encryption to this function"""
        """
        read_data = self.read_data()
        try:
            decr_data = f.decrypt(read_data.encode())
            user_data = decr_data.decode()
            print("User data: " + user_data)
            return user_data
        except InvalidToken:
            print("Improperly encrypted data received: " + read_data)
            logging.info("Improperly encrypted data received")
            return """""
        return self.read_data()

    def read_data(self) -> str:
        """Reads the data input from the RFID"""
        try:
            tag_id, user_info = self.reader.read()
        finally:
            GPIO.cleanup()
        # TODO add a logger for all tag_ids added
        return user_info

    def write_user_to_tag(self, user: User):
        """Writes new user info to an RFID tag. Waits for a tag to contact.
        Written info format:
        'entered_username|last_login_datetime('%Y-%m-%d %H:%M:%S')' """
        # user_info = self.encrypt_user_data(user)
        user_info = self.get_user_data(user)

        try:
            self.reader.write(str(user_info))
        finally:
            GPIO.cleanup()

    """def encrypt_user_data(self, user: User) -> bytes:
        Encrypts a user's information into a token
        user_info = self.get_user_data(user)
        
        user_info = user_info[0:-1]
        user_bytes = user_info.encode()
        encr_user_data = f.encrypt(user_bytes)
        print("User data encrypted to" + str(encr_user_data))

        return encr_user_data"""

    def get_user_data(self, user: User):
        """Gets a string representation of the user's info"""
        user_info = ""
        attributes = [
            user.get_username(),
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            user.get_key()
        ]

        for attribute in attributes:
            user_info += str(attribute)
            user_info += "|"

        return user_info[0:-1]
