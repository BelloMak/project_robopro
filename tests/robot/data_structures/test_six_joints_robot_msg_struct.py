import math
import struct

from roboter.common.error.custom_error import Error
from roboter.robot.message_data_structures.six_joints_robot_msg_struct import (
    SixJointsRobotAnglesData,
)

NUMBER_OF_JOINTS = 6
FORMAT = "Q" + "d" * NUMBER_OF_JOINTS
TIMESTAMP = 123456
DATA = (179.0, 223.0, -74.0, 35.0, 65.0, 0.0)
DATA_RAD = tuple([math.radians(i) for i in DATA])


def test_unpack():
    raw_data = struct.pack(FORMAT, TIMESTAMP, *DATA)
    data, error = SixJointsRobotAnglesData.unpack(raw_data)
    assert error is None
    assert data is not None
    assert data.identifier == TIMESTAMP
    assert data.angles == DATA_RAD


def test_unpack_error_because_wrong_data_format():
    raw_data = struct.pack("dd", *(123.0, 456.0))
    data, error = SixJointsRobotAnglesData.unpack(raw_data)
    assert isinstance(error, Error)
    assert data is None
