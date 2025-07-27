import math
import struct
from typing import Optional, Tuple

from roboter.common.error.custom_error import Error
from roboter.common.error.data_type_error import DataTypeError
from roboter.robot.message_data_structures.interface.i_message_structure import (
    IAnglesData,
)


class SixJointsRobotAnglesData(IAnglesData):
    NUMBER_OF_JOINTS = 6
    UNPACK_FORMAT = "Q" + "d" * NUMBER_OF_JOINTS

    identifier: int
    angles: Tuple[float, float, float, float, float, float]

    def __init__(self):
        self.identifier = 0
        self.angles = (0, 0, 0, 0, 0, 0)

    @classmethod
    def unpack(
        cls, data: bytes
    ) -> Tuple[Optional[IAnglesData], Optional[Error]]:
        """
        Unpack six joints robot angles data.
        """

        try:
            unpacked_data = struct.unpack(cls.UNPACK_FORMAT, data)
            new_obj = SixJointsRobotAnglesData()
            new_obj.identifier = unpacked_data[0]
            new_obj.angles = (
                math.radians(unpacked_data[1]),
                math.radians(unpacked_data[2]),
                math.radians(unpacked_data[3]),
                math.radians(unpacked_data[4]),
                math.radians(unpacked_data[5]),
                math.radians(unpacked_data[6]),
            )
            return new_obj, None
        except struct.error:
            return None, DataTypeError("failed to unpack data, wrong format")

    @classmethod
    def get_message_size(cls) -> int:
        """
        Get data message length in bytes.
        """

        return struct.calcsize(cls.UNPACK_FORMAT)
