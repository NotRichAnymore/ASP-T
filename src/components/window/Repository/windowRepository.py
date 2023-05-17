import logging
import pysnooper

from src.components.window.Models.windowManager import WindowManager

@pysnooper.snoop()
class WindowRepository:
    def __init__(self, logger):
        self.logger = logger
        self.model = WindowManager()

    def get_active_window_manager(self):
        return self.model.get_active_window_manager()

    def set_window_manager_variables(self, previous, active, status):
        self.model.set_previous_window(previous)
        self.model.set_active_window(active)
        self.model.set_gui_status(status if status is not None else True)

