

class WindowManager:
    def __init__(self):
        self.window_manager = {'previous_window': '', 'active_window': '', 'gui_status': None}

    def set_previous_window(self, previous_window):
        self.window_manager['previous_window'] = previous_window

    def set_active_window(self, active_window):
        self.window_manager['active_window'] = active_window

    def set_gui_status(self, gui_status):
        self.window_manager['gui_status'] = gui_status

    def get_previous_window(self):
        return self.window_manager['previous_window']

    def get_active_window(self):
        return self.window_manager['active_window']

    def get_gui_status(self):
        return self.window_manager['gui_status']

    def get_active_window_manager(self):
        return self.window_manager

