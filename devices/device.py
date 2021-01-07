from abc import abstractmethod


class Device:
    """An external device"""

    @abstractmethod
    def is_on(self) -> bool:
        pass



