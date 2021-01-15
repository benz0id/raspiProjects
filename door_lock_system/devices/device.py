from abc import abstractmethod


class Device:
    """An external device"""

    @abstractmethod
    def is_running(self) -> bool:
        pass



