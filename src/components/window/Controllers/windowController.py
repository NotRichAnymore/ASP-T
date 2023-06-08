import logging

import pysnooper


class WindowController:
    def __init__(self, service, logger):
        self.service = service
        self.logger = logger

    def get_active_window_manager(self):
        return self.service.get_window_manager()

    def get_active_window(self):
        window_manager = self.get_active_window_manager()
        return window_manager['active_window']

    def update_active_window_(self, previous, active, status=None):
        self.service.update_window_manager(previous, active, status)

    # @pysnooper.snoop()
    def save_console_output(self, settings, output):
        self.logger.create_log_entry(level=logging.DEBUG, message='Saving console output')
        self.service.write_output_to_file(settings, output)

    # @pysnooper.snoop()
    def load_console_output(self):
        self.logger.create_log_entry(level=logging.DEBUG, message='Loading console output')
        return self.service.read_output_file()
