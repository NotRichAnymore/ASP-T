import logging


import pysnooper


class SettingsService:
    def __init__(self, repo, validator, logger):
        self.repository = repo
        self.validator = validator
        self.object_loaded = None
        self.logger = logger

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

    def present(self, path):
        path_present = self.validator.path_present(self.object_loaded, path)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Path present: {path_present}')
        return path_present

    def change_current_theme(self, theme):
        return self.repository.set_theme(theme)

    def get_default_theme(self):
        return self.repository.default_theme()

    def get_previous_theme(self):
        return self.repository.get_last_theme()

    @pysnooper.snoop()
    def establish_theme(self, new_theme=None):
        previous_theme, current_theme = self.repository.get_themes()
        theme_status = self.validator.theme_status(previous_theme, current_theme, new_theme)
        match theme_status:
            case 'default':
                self.repository.change_theme_order(default=True)
            case 'update_default':
                self.repository.change_theme_order(previous=current_theme, current=new_theme)
            case 'update':
                self.repository.change_theme_order(previous=current_theme, current=new_theme)

        updated_previous_theme, updated_current_theme = self.repository.get_themes()
        return updated_current_theme

    @pysnooper.snoop()
    def establish_save_folder(self, new_save_folder):
        save_folder = self.repository.get_save_folder()
        if self.repository.validate.save_folder(new_save_folder, save_folder):
            self.repository.change_save_folder(new_save_folder)
            return self.repository.create_existing_settings()
