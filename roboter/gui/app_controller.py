from roboter.gui.app_model import AppModel
from roboter.gui.app_view import AppView


class AppController(object):
    """
    Controller class of MVVM-C design pattern.
    """

    def __init__(self, app_model: AppModel, app_view: AppView):
        self._app_model = app_model
        self._app_view = app_view

    def handle_get_end_effector_position(self):
        """
        Handler for event, that caused get end effector position calculation.
        """

        view_model = self._app_view.get_view_model()

        result, err = self._app_model.get_end_effector_position()

        if err is not None or result is None:
            view_model.show_get_end_effector_pos_error()
        else:
            view_model.clear_error_label()
            data = []
            for item in result:
                row = []
                for value in tuple(item):
                    if isinstance(value, float):
                        row.append("{:.6f}".format(value))
                    else:
                        row.append(str(value))
                data.append(tuple(row))
            view_model.add_rows(data)

        self._app_view.render(view_model)

    def handle_clear_table(self):
        """
        Handler for event, that caused clear table.
        """

        view_model = self._app_view.get_view_model()
        view_model.clear_rows()

        self._app_view.render(view_model)
