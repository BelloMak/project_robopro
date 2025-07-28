from typing import Iterable, Optional, Tuple

from roboter.common.error.app_model_error import AppModelError
from roboter.robot_controller.robot_controller import (
    PositionData,
    RobotController,
)


class AppModel(object):
    """
    Model class of MVVM-C design pattern.
    """

    def __init__(self, robot_controller: RobotController):
        self.robot_controller = robot_controller

    def get_end_effector_position(
        self,
    ) -> Tuple[Optional[Iterable[PositionData]], Optional[AppModelError]]:
        """
        Get robot end effector position.
        """
        result, err = self.robot_controller.get_robot_position()

        if err is not None:
            return None, AppModelError(
                f"failed to get end effector position: {err.message}"
            )
        return result, None
