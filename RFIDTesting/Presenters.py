
# TODO add functionality for a display
from abc import abstractmethod
from logging import warning

import LCDDriver
from typing import List


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


class LCD(Presenter):

    lcd: LCDDriver.lcd
    LINE_LENGTH = 20
    NUM_LINES = 4

    def __init__(self):
        """Creates a new LCD driver"""
        self.lcd = LCDDriver.lcd()

    def to_lines_list(self, to_break: str) -> List[str]:
        """Breaks a <to_break> into multiple strings based upon the placement of
        newline characters"""
        broken_strs = [""]
        i = 0
        j = 0

        while j < len(to_break):
            if to_break[j] == "\\" and to_break[j + 1] == "n":
                i += 1
                print("adding a new index" + str(i))
                broken_strs[i] = ""
                j += 1
            else:
                broken_strs[i] += to_break[j]
            j += 1

        for s in to_break:
            if len(s) > self.LINE_LENGTH:
                warning("LCD line length exceeded.\n Max: " +
                        str(self.LINE_LENGTH) + "\nReached: " + str(len(s)) +
                        "\nOffending line \"" + s + "\"")
        if len(broken_strs) > self.NUM_LINES:
            warning("Number of LCD lines exceeded.\n Max: " +
                    str(self.NUM_LINES) + "\nReached: " + str(len(broken_strs)) +
                    "\nOffending message: \"" + to_break + "\"")

        return broken_strs

    def print(self, to_show: str):
        """Shows the given string on the the LCD"""
        str_list = self.to_lines_list(to_show)
        print("Printing to LCD")
        for i in range(len(str_list)):
            print("Printing:" + str_list[i] + "at index " + str(i))
            self.lcd.lcd_display_string(str_list[i], i)

    def input(self, to_show: str) -> str:
        """Shows the text to the user and fetches their input."""
        self.print(to_show)
        # TODO this should be fixed using a keyboard input source
        return input()




