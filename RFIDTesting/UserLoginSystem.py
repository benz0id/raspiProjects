import base64

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
from cryptography.fernet import Fernet
# import cryptography.fernet
from UserInfo import UserInfo
from time import sleep

# f = Fernet(b'opEKlFMJK955SESMBvK4s_ioW2w-gUUzZ8F5XBJZzYg=')
reader = SimpleMFRC522()


# User String Format
# username | lastlogin

def write_new_username():
    user_txt = input("No Valid User-Key detected, enter a new username:")
    print("Now place your tag to write")
    write_username_curtime(user_txt)
    print("Welcome, " + user_txt)


def write_username_curtime(username: str):
    try:
        reader.write((username + "|" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    finally:
        GPIO.cleanup()


def valid_data(read_data: str):
    if read_data.find("|") > -1:
        return read_data
    else:
        return ""


def load_user(user_str: str) -> bool:
    try:
        user = UserInfo(user_str)
        user.get_login_str()
        write_username_curtime(user.name)
        print(user.get_login_str())
        return True
    except ValueError:
        return False


while True:
    try:
        id, data = reader.read()
        data = data.strip()
        is_data = valid_data(data)
        valid_key = bool(is_data and load_user(is_data))
        if not valid_key:
            write_new_username()

    finally:
        GPIO.cleanup()
