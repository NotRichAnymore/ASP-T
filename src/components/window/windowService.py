from pathlib import Path
import logging
import pysnooper


@pysnooper.snoop()
class WindowService:
    def __init__(self, repo, validator, logger):
        self.repository = repo
        self.validator = validator
        self.logger = logger
        self.save_path = None

    def get_window_manager(self):
        return self.repository.get_active_window_manager()

    def update_window_manager(self, previous, active, status):
        self.repository.set_window_manager_variables(previous, active, status)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Updating window manager: '
                                                                  f'{previous}, {active}, {status}')

    def write_output_to_file(self, settings, output):
        save_folder = settings['Files']['save_folder']
        save_path = Path(save_folder).joinpath('console_output.txt')
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Using {save_path}')
        self.save_path = save_path
        with open(save_path, 'w+') as output_file:
            output_file.writelines(output)
            self.logger.create_log_entry(level=logging.DEBUG, message=f'Console Output written to {save_path}')

    def read_output_file(self):
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Reading from {self.save_path}')
        with open(self.save_path, 'r') as output_file:
            return output_file.readlines()
