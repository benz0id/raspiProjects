import random


class SecurityManager:

    KEY = 119218851371

    def __init__(self):
        if self.KEY == 119218851371:
            raise UserWarning("Default key - used change "
                              "in security_manager.py")

    def validate_key(self, code: int) -> bool:
        """Returns True iff the <code> is divisible by the KEY"""
        return code % self.KEY == 0

    def generate_key(self):
        """Generates a new key using the KEY which will return true when parsed
        by validate_key."""
        return self.KEY * random.randint(0, 1000)
