from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple

from roboter.common.error.custom_error import Error

ReceiveResult = Tuple[Optional[bytes], bool]
# [bytes, bool] - [raw_data, has_received]


class IReadStream(object, metaclass=ABCMeta):
    """
    Class that can only read data from stream.
    """

    @abstractmethod
    def open(self) -> Optional[Error]:
        """
        Open stream, aka connect.
        """

    @abstractmethod
    def send_data(self, data: bytes) -> Optional[Error]:
        """
        Method to send data to the stream.
        """

    @abstractmethod
    def close(self) -> Optional[Error]:
        """
        Close stream, aka disconnect.
        """


class IWriteStream(object, metaclass=ABCMeta):
    """
    Class that can only write data from stream.
    """

    @abstractmethod
    def open(self) -> Optional[Error]:
        """
        Open stream, aka connect.
        """

    @abstractmethod
    def receive_data(
        self, buffer_size: int = 0
    ) -> Tuple[ReceiveResult, Optional[Error]]:
        """
        Method to receive data from stream.
        """

    @abstractmethod
    def close(self) -> Optional[Error]:
        """
        Close stream, aka disconnect.
        """


class IStream(IReadStream, IWriteStream, metaclass=ABCMeta):
    """
    Class that can read and write data from stream.
    """
