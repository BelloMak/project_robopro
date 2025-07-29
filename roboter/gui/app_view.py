from typing import Callable, Tuple

from PyQt6 import QtWidgets

from roboter.gui.app_view_model import AppViewModel
from roboter.gui.gui_layout import Ui_MainWindow


class AppView(Ui_MainWindow):
    """
    View class of MVVM based design architecture.
    """

    def __init__(self):
        super().__init__()
        self._view_model = AppViewModel()
        self._main_window = QtWidgets.QMainWindow()

        self.setupUi(self._main_window)
        self.retranslateUi(self._main_window)
        self._render()

    def on_get_robot_position_click(self, callback: Callable):
        """
        Setter for get robot position click event.
        """
        self.getRobotPositionButton.clicked.connect(callback)

    def on_clear_table_click(self, callback: Callable):
        """
        Setter for clear table click event.
        """
        self.clearButton.clicked.connect(callback)

    def show(self):
        """
        Show application window.
        """
        self._main_window.show()

    def get_view_model(self) -> AppViewModel:
        """
        Getter for view model.
        """
        return self._view_model

    def render(self, view_model):
        """
        Render application window.
        """
        self._view_model = view_model
        self._render()

    def _render(self):
        """
        Render application window.
        """
        self.tableWidget.clearContents()
        self._delete_rows()
        self._create_rows(len(self._view_model.rows))

        for i, row_data in enumerate(self._view_model.rows):
            self._fill_table_row(i, row_data)
        self.tableWidget.scrollToBottom()

        self.errorLabel.setText("")
        if self._view_model.error_label is not None:
            self.errorLabel.setText(self._view_model.error_label)

    def _create_rows(self, number):
        """
        Create specified number of rows.
        """
        for i in range(self.tableWidget.rowCount(), number):
            self.tableWidget.insertRow(i)

    def _fill_table_row(
        self, row, data: Tuple[str, str, str, str, str, str, str]
    ):
        """
        Fill specified table row with provided data.
        """
        for i, data_item in zip(range(self.tableWidget.columnCount()), data):
            self.tableWidget.setItem(
                row, i, QtWidgets.QTableWidgetItem(data_item)
            )

    def _delete_rows(self):
        """
        Remove all rows from table.
        """
        self.tableWidget.setRowCount(0)
