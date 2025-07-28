class Error(object):
    """
    Custom error class for module
    """

    def __init__(self, message: str = ""):
        self._message = message

    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self.message()
