from abc import abstractmethod

from design_patterns.observer import Subject


class Device(Subject):
    """An external device"""

    @abstractmethod
    def is_running(self) -> bool:
        pass



