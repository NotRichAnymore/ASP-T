

class Settings:
    def __init__(self):
        self.config_path = None
        self.current_theme = None
        self.previous_theme = None
        self.folder = None
        self.user_details = None

    def get_path(self):
        return self.config_path

    def get_folder(self):
        return self.folder

    def get_user_details(self):
        return self.user_details

    def get_current_theme(self):
        return self.current_theme

    def get_previous_theme(self):
        return self.previous_theme

    def set_current_theme(self, theme):
        self.current_theme = theme

    def set_previous_theme(self, theme):
        self.previous_theme = theme

    def set_folder(self, folder):
        self.folder = folder

    def set_path(self, path):
        self.config_path = path

    def set_user_details(self, path):
        self.user_details = path
