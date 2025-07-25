from roboter.common.error.custom_error import Error


def test_with_message():
    error = Error("Test message")
    assert error.message() == "Test message"


def test_with_empty_string():
    error = Error("")
    assert error.message() == ""


def test_with_none_message():
    error = Error()
    assert error.message() == ""
