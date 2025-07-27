from typing import Optional, Tuple

from roboter.common.error.custom_error import Error
from roboter.robot.joint.interface.i_joint import IJoint, Matrix
from roboter.robot.robot_utils.robot_utils import (
    get_dh_transform_matrix,
)


class RevoluteJoint(IJoint):
    def __init__(self, a: float, d: float, alpha: float):
        """
        Create revolute joint object where a(m), d(m) and alpha(rad) - DH
        params.
        """
        self._a = a
        self._d = d
        self._alpha = alpha

    def get_matrix(
        self, variable_param: float
    ) -> Tuple[Optional[Matrix], Optional[Error]]:
        """
        Get DH matrix for specified theta angle in radians.
        """
        matrix = get_dh_transform_matrix(
            a=self._a, d=self._d, alpha=self._alpha, theta=variable_param
        )
        return matrix, None
