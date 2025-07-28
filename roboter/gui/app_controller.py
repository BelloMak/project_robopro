from roboter.gui.app_model import AppModel
from roboter.gui.app_view import AppView


class AppController(object):
    def __init__(self, app_model: AppModel, app_view: AppView):
        self._app_model = app_model
        self._app_view = app_view

    def handle_get_end_effector_position(self):
        view_model = self._app_view.get_view_model()

        result, err = self._app_model.get_end_effector_position()

        if err is not None or result is None:
            view_model.show_get_end_effector_pos_error()
        else:
            view_model.clear_error_label()
            view_model.add_rows(result)

        self._app_view.render(view_model)
