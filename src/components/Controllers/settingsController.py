


class SettingsController:
    def __init__(self, service):
        self.service = service

    def load_settings(self, default_path, path=None):
        if not self.settings_present(path):
            return self.service.create_new_settings_obj(default_path)
        return self.service.existing_settings_obj(path)

    def settings_present(self, path=None):
        return self.service.present(path)

    def update_theme(self, theme):
        return self.service.change_current_theme(theme)

    def manage_theme(self, theme):
        return self.service.establish_theme(theme)

