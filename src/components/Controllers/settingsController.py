


class SettingsController:
    def __init__(self, service):
        self.service = service

    def load_settings(self, path=None):
        if not self.settings_present():
            return self.service.create_new_settings_obj()
        return self.service.existing_settings_obj(path)

    def settings_present(self):
        return self.service.present()

    def update_theme(self, theme):
        return self.service.change_current_theme(theme)
