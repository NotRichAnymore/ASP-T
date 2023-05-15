from pathlib import Path
import pysnooper


class WindowController:
    def __init__(self):
        self.active_window_manager = {'previous_window': '', 'active_window': '', 'gui_status': None}
        self.save_path = None

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



    @pysnooper.snoop()
    def save_console_output(self, settings, output):
        save_folder = settings['Files']['save_folder']
        save_path = Path(save_folder).joinpath('console_output.txt')
        self.save_path = save_path
        with open(save_path, 'w+') as output_file:
            output_file.writelines(output)

    @pysnooper.snoop()
    def load_console_output(self):
        with open(self.save_path, 'r') as output_file:
            return output_file.readlines()
