from typing import List, Optional, Tuple

import numpy as np

from roboter.common.error.custom_error import Error
from roboter.common.error.data_type_error import DataTypeError
from roboter.common.logger.logger import debug
from roboter.robot.interface.i_robot import CoordinateSystemPosition, IRobot
from roboter.robot.joint.interface.i_joint import IJoint, Matrix
from roboter.robot.robot_utils.robot_utils import (
    get_coordinates_transform_matrix,
)


class Robot(IRobot):
    def __init__(self):
        self._base_position: CoordinateSystemPosition = (
            CoordinateSystemPosition(0, 0, 0, 0, 0, 0)
        )
        self._ee_position: CoordinateSystemPosition = CoordinateSystemPosition(
            0, 0, 0, 0, 0, 0
        )
        self._joints: List[IJoint] = []

        self.__base_translation_matrix = None
        self.__ee_translation_matrix = None

    def set_base_position(
        self, base_pos: CoordinateSystemPosition
    ) -> Optional[Error]:
        """
        Set robot base position.
        """

        self._base_position = base_pos
        self.__base_translation_matrix = None
        debug(f"Setted robot base position: {base_pos}")
        return None

    def set_end_effector_pos(
        self, ee_pos: CoordinateSystemPosition
    ) -> Optional[Error]:
        """
        Set end effector position in last joint coordinates.
        """

        self._ee_position = ee_pos
        self.__ee_translation_matrix = None
        debug(f"Setted robot end effector position: {ee_pos}")
        return None

    def add_joint(self, joint: IJoint) -> Optional[Error]:
        """
        Add joint to robot.
        """

        self._joints.append(joint)
        debug(
            f"Added new joint to robot, joints quantity: {len(self._joints)}"
        )
        return None

    def get_ee_position(
        self, joints_pos: Tuple[float, ...]
    ) -> Tuple[Optional[Matrix], Optional[Error]]:
        """
        Calculate end effector position using joints positions.
        """

        matrix, err = self._get_transform_matrix(joints_pos)
        if err is not None or matrix is None:
            return None, err
        return matrix, None

    def _get_transform_matrix(
        self, joints_pos: Tuple[float, ...]
    ) -> Tuple[Optional[Matrix], Optional[Error]]:
        """
        Get transformation matrix for all joints
        """

        if len(joints_pos) != len(self._joints):
            return None, DataTypeError("invalid input data length")
        # base pos matrix
        if self.__base_translation_matrix is None:
            self.__base_translation_matrix = get_coordinates_transform_matrix(
                self._base_position.x,
                self._base_position.y,
                self._base_position.z,
                self._base_position.alpha,
                self._base_position.beta,
                self._base_position.gamma,
            )
        # robot joints translation matrix
        matrix = self.__base_translation_matrix
        for joint, joint_pos in zip(self._joints, joints_pos):
            matrix_i, err = joint.get_matrix(joint_pos)
            if err is not None or matrix_i is None:
                return None, err
            matrix = np.dot(matrix, matrix_i)
        # end effector translation matrix
        if self.__ee_translation_matrix is None:
            self.__ee_translation_matrix = get_coordinates_transform_matrix(
                self._ee_position.x,
                self._ee_position.y,
                self._ee_position.z,
                self._ee_position.alpha,
                self._ee_position.beta,
                self._ee_position.gamma,
            )

        matrix = np.dot(matrix, self.__ee_translation_matrix)

        return matrix, None
