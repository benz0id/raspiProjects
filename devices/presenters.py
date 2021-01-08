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
    """A class capable of displaying information to the user"""

    @abstractmethod
    def print(self, to_show: str):
        """Displays <to_show> to the user"""
        return NotImplemented

    @abstractmethod
    def input(self, to_show: str) -> str:
        """Shows <to_show> and collects the user input"""
        return NotImplemented


class ConsolePresenter(Presenter):
    """A presenter that prints to the console"""

    def print(self, to_show: str):
        """Displays the given text through the console"""
        print(to_show)

    def input(self, to_show: str) -> str:
        """Shows the given text and collects the user input through the
        console"""
        return input(to_show)


class LCD(Presenter):
    """An LCD presenter
    === Private Attributes ===
    _lcd_regulator:
            A thread that regulates the amount of time the LCD stays on.
    _LCD_ON_TIME = 30
            The amount of time the LCD spends turned on before shutting off
    _last_turned_on: datetime
            The last time the LCD was tuned on.
    _lcd: lcd_driver.lcd
            The LCD driver
    _LINE_LENGTH = 20
            The length of each line on the LCD
    _NUM_LINES = 4
            The number of lines available in the LCD
    """

    _lcd_regulator: Thread
    _LCD_ON_TIME = 30
    _last_turned_on: datetime

    _lcd: lcd_driver.lcd
    _LINE_LENGTH = 20
    _NUM_LINES = 4

    def __init__(self):
        self._lcd = lcd_driver.lcd()
        self._lcd_regulator = Thread(target=self.check_lcd)
        self._last_turned_on = datetime.now()

    def check_lcd(self):
        """Check if the lcd is currently being used, if the lcd hasn't been used
        in LCD_ON_TIME seconds, then it is turned off. Checks every 30 seconds.
        """
        while self._lcd.is_on:
            sleep(10)
            mutex.acquire()
            if datetime.now() - self._last_turned_on > \
                    timedelta(0, self._LCD_ON_TIME):
                self._lcd.lcd_clear()
                self._lcd.backlight(0)
            mutex.release()

    def begin_off_timer(self):
        """If it is not already running begins the thread that regulates the
        lcd"""
        mutex.acquire()
        self._lcd.lcd_clear()
        self._lcd.backlight(1)
        self._last_turned_on = datetime.now()
        if not self._lcd_regulator.is_alive():
            self._lcd_regulator = Thread(target=self.check_lcd)
            self._lcd_regulator.start()
        mutex.release()

    def print(self, to_show: str):
        """Shows the given string on the the lcd"""
        str_list = self.to_lines_list(to_show)
        self.begin_off_timer()
        logging.info("Printing to lcd")
        try:
            for i in range(len(str_list)):
                logging.info("Printing:" + str_list[i][0:20] + " at index " +
                             str(i))
                if len(str_list[i]) > self._NUM_LINES:
                    logging.info("Overhang:" + str_list[i][20:])
                self._lcd.lcd_display_string(str_list[i], i)
        except IOError:
            logging.error("Failed to print to lcd")

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

        while j < len(to_break):
            if to_break[j] == "\n":
                i += 1
                logging.info("adding a new index" + str(i))
                broken_strs.append("")
            else:
                broken_strs[i] += to_break[j]
            j += 1

        for s in to_break:
            if len(s) > self._LINE_LENGTH:
                warning("lcd line length exceeded.\n Max: " +
                        str(self._LINE_LENGTH) + "\nReached: " + str(len(s)) +
                        "\nOffending line \"" + s + "\"")
        if len(broken_strs) > self._NUM_LINES:
            warning("Number of lcd lines exceeded.\n Max: " +
                    str(self._NUM_LINES) + "\nReached: " + str(
                len(broken_strs)) +
                    "\nOffending message: \"" + to_break + "\"")

        return broken_strs
