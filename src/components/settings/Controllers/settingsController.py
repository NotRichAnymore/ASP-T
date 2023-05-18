import logging


class SettingsController:
    def __init__(self, service, logger):
        self.service = service
        self.logger = logger

    def load_settings(self, default_path, path=None):
        if not self.settings_present(path):
            self.logger.create_log_entry(
                level=logging.CRITICAL, message='Existing settings not found. Creating new settings')
            return self.service.create_new_settings_obj(default_path)
        self.logger.create_log_entry(level=logging.CRITICAL, message=f'Settings exist, using {path} to create settings')
        return self.service.existing_settings_obj(path)

    def settings_present(self, path=None):
        return self.service.present(path)

    def update_theme(self, theme):
        return self.service.change_current_theme(theme)

    def manage_theme(self, theme):
        return self.service.establish_theme(theme)

    def manage_save_folder(self, save_folder):
        return self.service.establish_save_folder(save_folder)

    def set_user_credentials(self, username, password):
        return self.service.credential_handling(username, password)

