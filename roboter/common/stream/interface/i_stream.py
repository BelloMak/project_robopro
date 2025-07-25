from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple

from roboter.common.error.custom_error import Error

ReceiveResult = Tuple[bytes, bool]
# [bytes, bool] - [raw_data, has_received]


class IReadStream(object, metaclass=ABCMeta):
    @abstractmethod
    def send_data(self, data: bytes) -> Optional[Error]:
        """
        Method to send data to the stream.
        """
        pass


class IWriteStream(object, metaclass=ABCMeta):
    @abstractmethod
    def receive_data(self) -> Tuple[ReceiveResult, Optional[Error]]:
        """
        Method to receive data from stream.
        """
        pass
