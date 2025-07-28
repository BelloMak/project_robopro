from typing import Iterable, List, Optional, Tuple

from roboter.robot_controller.robot_controller import (
    PositionData,
)


class AppViewModel(object):
    GET_END_EFFECTOR_POS_ERROR = "Failed to get end effector position!"

    def __init__(self):
        self.rows: List[
            Tuple[int, float, float, float, float, float, float]
        ] = []
        self.error_label: Optional[str] = None

    def add_rows(self, rows: Iterable[PositionData]):
        for row in rows:
            self.rows.append(tuple(row))

    def clear_rows(self):
        self.rows = []

    def show_get_end_effector_pos_error(self):
        self.error_label = self.GET_END_EFFECTOR_POS_ERROR

    def clear_error_label(self):
        self.error_label = None
