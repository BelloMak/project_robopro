from roboter.common.error.custom_error import CustomError


def test_with_message():
    error = CustomError("Test message")
    assert error.message() == "Test message"


def test_with_empty_string():
    error = CustomError("")
    assert error.message() == ""


def test_with_none_message():
    error = CustomError()
    assert error.message() == ""
