from abc import abstractmethod
from DPs.observer import Subject


class Device(Subject):
    """An external device"""

    @abstractmethod
    def is_running(self) -> bool:
        pass



