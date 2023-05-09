class WindowController:
    def __init__(self):
        self.active_window_manager = {'previous_window': '', 'active_window': '', 'gui_status': None}

    def get_active_window_manager(self):
        return self.active_window_manager

    def update_active_window_(self, previous, active, status=None):
        self.active_window_manager = {'previous_window': previous, 'active_window': active,
                                      'gui_status': status if status is not None else True}

    def get_previous_window(self):
        return self.active_window_manager['gui_status']

    def get_active_window(self):
        return self.active_window_manager['active_window']

    def get_active_window_status(self):
        return self.active_window_manager['gui_status']
