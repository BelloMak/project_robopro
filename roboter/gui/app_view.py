from typing import Callable, Tuple

from PyQt6 import QtWidgets

from roboter.gui.app_view_model import AppViewModel
from roboter.gui.gui_layout import Ui_MainWindow


class AppView(Ui_MainWindow):
    def __init__(self, view_model: AppViewModel):
        super().__init__()
        self._view_model = view_model
        self._main_window = QtWidgets.QMainWindow()

        self.setupUi(self._main_window)
        self.retranslateUi(self._main_window)
        self._render()

    def on_get_robot_position_click(self, callback: Callable):
        self.pushButton.clicked.connect(callback)

    def show(self):
        self._main_window.show()

    def get_view_model(self) -> AppViewModel:
        return self._view_model

    def render(self, view_model):
        self._view_model = view_model
        self._render()

    def _render(self):
        self.tableWidget.clearContents()
        self._clear_rows()
        self._create_rows(len(self._view_model.rows))

        for i in range(len(self._view_model.rows)):
            self._fill_table_row(i, self._view_model.rows[i])

        self.tableWidget.scrollToBottom()

        self.errorLabel.setText("")
        if self._view_model.error_label is not None:
            self.errorLabel.setText(self._view_model.error_label)

    def _create_rows(self, number):
        for i in range(self.tableWidget.rowCount(), number):
            self.tableWidget.insertRow(i)

    def _fill_table_row(
        self, row, data: Tuple[int, float, float, float, float, float, float]
    ):
        for i, data_item in zip(range(self.tableWidget.columnCount()), data):
            self.tableWidget.setItem(
                row, i, QtWidgets.QTableWidgetItem(str(data_item))
            )

    def _clear_rows(self):
        self.tableWidget.setRowCount(0)
