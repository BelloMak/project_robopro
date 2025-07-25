from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple

from roboter.common.error.custom_error import Error


class IAnglesData(object, metaclass=ABCMeta):
    identifier: int
    angles: List[float]

    @classmethod
    @abstractmethod
    def unpack(cls, data: bytes) -> Tuple[object, Optional[Error]]:
        """
        Unpack raw data to structure.
        """

    @classmethod
    @abstractmethod
    def get_message_size(cls) -> int:
        """
        Get message length in bytes.
        """
