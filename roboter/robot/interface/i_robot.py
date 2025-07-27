from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional, Tuple

from roboter.common.error.custom_error import Error
from roboter.robot.joint.interface.i_joint import IJoint, Matrix


class CoordinateSystemPosition(NamedTuple):
    x: float  # (m)
    y: float  # (m)
    z: float  # (m)
    alpha: float  # rotation around x (rad)
    beta: float  # rotation around y (rad)
    gamma: float  # rotation around z (rad)


class IRobot(object, metaclass=ABCMeta):
    @abstractmethod
    def set_base_position(
        self, base_pos: CoordinateSystemPosition
    ) -> Optional[Error]:
        """
        Set robot base position.
        """

    @abstractmethod
    def set_end_effector_pos(
        self, ee_pos: CoordinateSystemPosition
    ) -> Optional[Error]:
        """
        Set end effector position in last joint coordinates.
        """

    @abstractmethod
    def add_joint(self, joint: IJoint) -> Optional[Error]:
        """
        Add joint to robot.
        """

    @abstractmethod
    def get_ee_position(
        self, joints_pos: Tuple
    ) -> Tuple[Optional[Matrix], Optional[Error]]:
        """
        Calculate end effector position using joints positions.
        """
