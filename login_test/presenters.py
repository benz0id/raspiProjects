# TODO add functionality for a display
import logging
from abc import abstractmethod
from logging import warning
from threading import Thread, Lock
from datetime import datetime, timedelta
from time import sleep
import lcd_driver
from typing import List

mutex = Lock()


class Presenter:

    @abstractmethod
    def print(self, to_show: str):
        """Displays <to_show> to the user"""
        return NotImplemented

    @abstractmethod
    def input(self, to_show: str) -> str:
        """Shows <to_show> and collects the user input"""
        return NotImplemented


class SimplePresenter(Presenter):

    def print(self, to_show: str):
        """Displays the given text through the console"""
        print(to_show)

    def input(self, to_show: str) -> str:
        """Shows the given text and collects the user input through the
        console"""
        return input(to_show)


# Characteristics of the LCD

LCD_ON_TIME = 30
LINE_LENGTH = 20
NUM_LINES = 4


class LCD(Presenter):
    lcd_regulator: Thread
    last_turned_on: datetime
    lcd: lcd_driver.lcd

    def __init__(self):
        self.lcd = lcd_driver.lcd()
        self.lcd_regulator = Thread(target=self.check_lcd)
        self.last_turned_on = datetime.now()

    def check_lcd(self):
        """Check if the LCD is currently being used, if the lcd hasn't been used
        in LCD_ON_TIME seconds, then it is turned off. Checks every 30 seconds.
        """
        while self.lcd.is_on:
            sleep(10)
            mutex.acquire()
            if datetime.now() - self.last_turned_on > \
                    timedelta(0, LCD_ON_TIME):
                self.lcd.lcd_clear()
                self.lcd.backlight(0)
            mutex.release()

    def begin_off_timer(self):
        """If it is not already running begins the thread that regulates the
        LCD"""
        mutex.acquire()
        self.lcd.lcd_clear()
        self.lcd.backlight(1)
        self.last_turned_on = datetime.now()
        if not self.lcd_regulator.is_alive():
            self.lcd_regulator = Thread(target=self.check_lcd)
            self.lcd_regulator.start()
        mutex.release()

    def print(self, to_show: str):
        """Shows the given string on the the LCD"""
        str_list = self.to_lines_list(to_show)
        self.begin_off_timer()
        logging.info("Printing to LCD")
        try:
            for i in range(len(str_list)):
                logging.info("Printing:" + str_list[i] + " at index " + str(i))
                self.lcd.lcd_display_string(str_list[i], i)
        except IOError:
            logging.error("Failed to print to LCD")

    def input(self, to_show: str) -> str:
        """Shows the text to the user and fetches their input."""
        self.print(to_show)
        # TODO this should be fixed using a keyboard input source
        return input()

    def to_lines_list(self, to_break: str) -> List[str]:
        """Breaks a <to_break> into multiple strings based upon the placement of
        newline characters"""
        broken_strs = [""]
        i = 0
        j = 0
        k = 0

        while j < len(to_break):
            if to_break[j] == "\n":
                i += 1
                broken_strs.append("")
                k = 0
                j += 1
            elif k >= LINE_LENGTH:
                i += 1
                k = 0
                broken_strs.append("")
            else:
                broken_strs[i] += to_break[j]
                j += 1
                k += 1

        for s in to_break:
            if len(s) > LINE_LENGTH:
                logging.warning("LCD line length exceeded.\n Max: " +
                                str(LINE_LENGTH) + "\nReached: " + str(len(s)) +
                                "\nOffending line \"" + s + "\"")
        if len(broken_strs) > NUM_LINES:
            logging.warning("Number of LCD lines exceeded.\n Max: " +
                            str(NUM_LINES) + "\nReached: " + str(
                len(broken_strs)) +
                            "\nOffending message: \"" + to_break + "\"")

        return broken_strs
