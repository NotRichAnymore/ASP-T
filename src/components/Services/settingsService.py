from pathlib import Path

import pysnooper


class SettingsService:
    def __init__(self, repo, validator):
        self.repository = repo
        self.validator = validator
        self.object_loaded = None

    def create_new_settings_obj(self, default_path):
        settings = self.repository.initialise_config_file(default_path)
        self.repository.set_initial_vars()
        self.object_loaded = True
        return settings

    def existing_settings_obj(self, path):
        settings = self.repository.get_settings_by_path(path)
        self.repository.set_initial_vars()
        self.object_loaded = True
        return settings

    def present(self, path=None):
        if path:
            return Path(path).exists()
        return False if not self.object_loaded or self.object_loaded is None else True

    def change_current_theme(self, theme):
        return self.repository.set_theme(theme)

    def get_default_theme(self):
        return self.repository.default_theme()

    def get_previous_theme(self):
        return self.repository.get_last_theme()

    @pysnooper.snoop()
    def establish_theme(self, new_theme=None):
        previous_theme, current_theme = self.repository.get_themes()
        if previous_theme is None and current_theme is None and \
                new_theme == 'SystemDefault' or new_theme == 'Default' or new_theme is None:
            self.repository.change_theme_order(default=True)

        if previous_theme is None and current_theme == 'SystemDefault':
            self.repository.change_theme_order(previous=current_theme, current=new_theme)

        if current_theme and previous_theme and new_theme:
            self.repository.change_theme_order(previous=current_theme, current=new_theme)

        updated_previous_theme, updated_current_theme = self.repository.get_themes()
        return updated_current_theme

    def establish_save_folder(self, new_save_folder):
        save_folder = self.repository.get_save_folder()
        if new_save_folder != save_folder and Path(new_save_folder).exists():
            self.repository.change_save_folder(save_folder)
            return self.repository.create_existing_settings()
