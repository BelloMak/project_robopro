from roboter.common.error.custom_error import Error


class RunTimeError(Error):
    def __init__(self, message: str = ""):
        super().__init__(message)
