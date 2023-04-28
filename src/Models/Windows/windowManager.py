class WindowManager:
    def __init__(self):
        self.active_window_manager = {'previous_window': '', 'active_window': '', 'gui_status': None}

    def get_active_window_manager(self):
        return self.active_window_manager

    def update_window_manager(self, previous, active, status):
        self.active_window_manager = {'previous_window': previous, 'active_window': active, 'gui_status': status}

    def get_previous_window(self):
        return self.active_window_manager['gui_status']

    def get_active_window(self):
        return self.active_window_manager['active_window']

    def get_active_window_status(self):
        return self.active_window_manager['gui_status']
