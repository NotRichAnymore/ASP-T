


class SettingsService:
    def __init__(self, repo, validator):
        self.repository = repo
        self.validator = validator
        self.object_loaded = None

    def create_new_settings_obj(self):
        settings = self.repository.initialise_config_file()
        self.object_loaded = True
        return settings

    def existing_settings_obj(self, path):
        settings = self.repository.get_settings_by_path(path)
        self.object_loaded = True
        return settings

    def present(self):
        return True if not self.object_loaded or self.object_loaded is not None else False

    def change_current_theme(self, theme):
        return self.repository.set_theme(theme)
