
# TODO add functionality for a display
from abc import abstractmethod


class Presenter:

    @abstractmethod
    def print(self, to_show: str):
        """Displays the given text"""
        return NotImplemented

    @abstractmethod
    def input(self, t):
        """Shows the given text and collects the user input"""
        return NotImplemented


class SimplePresenter(Presenter):

    def print(self, to_show: str):
        """Displays the given text through the console"""
        print(to_show)

    def input(self, to_show: str) -> str:
        """Shows the given text and collects the user input through the
        console"""
        return input(to_show)

