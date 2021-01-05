class InvalidInput(Exception):
    """Raised when input from the RFID tag does not match the expected
    formatting."""
    pass


class InvalidUserCode(Exception):
    """Raised when a user's code is invalid"""
    pass
