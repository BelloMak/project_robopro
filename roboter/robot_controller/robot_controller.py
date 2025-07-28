from typing import NamedTuple, Optional, Tuple

from roboter.common.error.connection_error import ConnectionError
from roboter.common.error.custom_error import Error
from roboter.common.stream.interface.i_stream import IStream
from roboter.robot.interface.i_robot import IRobot
from roboter.robot.message_data_structures.interface.i_message_structure_unpacker import (
    IJointsDataUnpacker,
)
from roboter.robot.robot_utils.robot_utils import (
    get_euler_angles_from_matrix,
    get_position_from_matrix,
)


class PositionData(NamedTuple):
    identifier: int  # some position identifier
    x: float  # x coordinate
    y: float  # y coordinate
    z: float  # x coordinate
    psi: float  # psi euler angle
    theta: float  # theta euler angle
    phi: float  # phi euler angle


def handle_connection(function):
    """
    Decorator, that implements open and close stream routine.
    """

    def wrapper(self, *args, **kwargs):
        err = self._stream.open()
        if err is not None:
            return None, err

        data, err = function(self, *args, **kwargs)

        if err is not None:
            return None, err

        _ = self._stream.close()
        return data, None

    return wrapper


class RobotController:
    __CMD_GET_POSITION = "get"

    def __init__(
        self, robot: IRobot, stream: IStream, unpacker: IJointsDataUnpacker
    ):
        self._robot = robot
        self._stream = stream
        self._unpacker = unpacker

    @handle_connection
    def get_robot_position(
        self,
    ) -> Tuple[Optional[Tuple[PositionData]], Optional[Error]]:
        """
        Get information about robot joints position: coordinates (x,y,z) and
        angles (psi, theta, phi) for the ZYX Euler transformation.
        """

        NUM_OF_MESSAGES = 5
        command = self.__CMD_GET_POSITION.encode("utf-8")
        result = []
        err = self._stream.send_data(command)
        if err is not None:
            return None, err

        for _ in range(NUM_OF_MESSAGES):
            (raw_data, has_received), err = self._stream.receive_data(
                buffer_size=self._unpacker.get_message_size(),
                timeout=1,
            )
            if err is not None:
                return None, err

            if not has_received or raw_data is None:
                return None, ConnectionError(
                    "failed to receive data from robot"
                )
            data, err = self._unpacker.unpack(raw_data)
            if err is not None or data is None:
                return None, err

            matrix, err = self._robot.get_ee_position(data.positions)

            if err is not None or matrix is None:
                return None, err

            positions, err = get_position_from_matrix(matrix)
            if err is not None or positions is None:
                return None, err
            angles, err = get_euler_angles_from_matrix(matrix)
            if err is not None or angles is None:
                return None, err

            result.append(PositionData(data.identifier, *positions, *angles))
        return tuple(result), None
