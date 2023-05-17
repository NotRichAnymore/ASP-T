import logging
from pathlib import Path


class SettingsValidator:
    def __init__(self, logger):
        self.logger = logger

    def path_present(self, object_loaded, path=None):
        if path:
            return Path(path).exists()
        return False if not object_loaded or object_loaded is None else True

    def theme_status(self, previous_theme, current_theme, new_theme):
        if previous_theme is None and current_theme is None and \
                new_theme == 'SystemDefault' or new_theme == 'Default' or new_theme is None:
            self.logger.create_log_entry(level=logging.DEBUG, message='Using Default Themes')
            return 'default'
        if previous_theme is None and current_theme == 'SystemDefault':
            self.logger.create_log_entry(level=logging.DEBUG, message='Updating Default Themes')
            return 'update_default'
        if current_theme and previous_theme and new_theme:
            self.logger.create_log_entry(
                level=logging.DEBUG, message=f'Updating Themes from {current_theme} to {new_theme}')
            return 'update'

    def validate_save_folder(self, new_save_folder, old_save_folder):
        if new_save_folder != old_save_folder and Path(new_save_folder).exists():
            self.logger.create_log_entry(level=logging.DEBUG, message=f'New save folder: {new_save_folder} valid')
            return True
        self.logger.create_log_entry(level=logging.DEBUG, message=f'New save folder {new_save_folder} not valid')
        return False
