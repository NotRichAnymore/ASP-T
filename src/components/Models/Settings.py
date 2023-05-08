class Settings:
    def __init__(self):
        self.config_path = None
        self.theme = None
        self.folder = None
        self.user_details = None

    def get_path(self):
        return self.config_path

    def set_path(self, path):
        self.config_path = path

    def get_theme(self):
        return self.theme

    def set_theme(self, theme):
        self.theme = theme

    def set_folder(self, folder):
        self.folder = folder

    def get_folder(self):
        return self.folder

    def set_user_details(self, path):
        self.user_details = path

    def get_user_details(self):
        return self.user_details
