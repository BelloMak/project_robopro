from typing import Iterable, List, Optional, Tuple

TableRow = Tuple[str, str, str, str, str, str, str]


class AppViewModel(object):
    """
    View Model class of MVVM-C design pattern.
    """

    GET_END_EFFECTOR_POS_ERROR = "Failed to get end effector position!"

    def __init__(self):
        self.rows: List[TableRow] = []
        self.error_label: Optional[str] = None

    def add_rows(self, rows: Iterable[TableRow]):
        """
        Add rows to table structure.
        """
        for row in rows:
            self.rows.append(row)

    def clear_rows(self):
        """
        Remove all rows from table structure.
        """
        self.rows = []

    def show_get_end_effector_pos_error(self):
        """
        Display specific error to user.
        """

        self.error_label = self.GET_END_EFFECTOR_POS_ERROR

    def clear_error_label(self):
        """
        Remove the error message display.
        """

        self.error_label = None
