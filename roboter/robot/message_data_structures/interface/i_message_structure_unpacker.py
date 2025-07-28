from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

from roboter.common.error.custom_error import Error


@dataclass(frozen=True)
class JointsData:
    identifier: int  # Specific message identifier
    positions: Tuple[float, ...]  # Joints position data (angles or linear pos)


class IJointsDataUnpacker(object, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def unpack(
        cls, data: bytes
    ) -> Tuple[Optional[JointsData], Optional[Error]]:
        """
        Unpack raw data to structure.
        """

    @classmethod
    @abstractmethod
    def get_message_size(cls) -> int:
        """
        Get message length in bytes.
        """
