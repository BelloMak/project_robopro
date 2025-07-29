from typing import Iterable, List, Optional, Tuple

TableRow = Tuple[int, float, float, float, float, float, float]
FormattedTableRow = Tuple[str, str, str, str, str, str, str]


class AppViewModel(object):
    """
    View Model class of MVVM based design architecture.
    """

    GET_END_EFFECTOR_POS_ERROR = "Failed to get end effector position!"

    def __init__(self):
        self.rows: List[FormattedTableRow] = []
        self.error_label: Optional[str] = None

    def add_rows(self, rows: Iterable[TableRow]):
        """
        Add rows to table structure.
        """
        for row in rows:
            formatted_row = []
            for item in tuple(row):
                if isinstance(item, float):
                    formatted_row.append("{:.6f}".format(item))
                else:
                    formatted_row.append(str(item))
            self.rows.append(tuple(formatted_row))

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
