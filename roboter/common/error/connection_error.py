from roboter.common.error.custom_error import Error


class ConnectionError(Error):
    def __init__(self, message: str = ""):
        super().__init__(message)
