import configupdater
import configparser
from pathlib import Path
from src.components.Utilities.utilities import create_error_message
from src.components.Models.Settings import Settings


class SettingsRepository:

    def __init__(self):
        self.model = Settings()
        self.updater = configupdater.ConfigUpdater()
        self.parser = configparser.ConfigParser()
        self.default_config_path = Path('src').resolve().parent.joinpath('data/files/config.ini').as_posix()

    def get_config_path(self):
        return self.model.get_path()

    def set_config_path(self, path):
        self.model.set_path(path)

    def get_current_theme(self):
        return self.model.get_theme()

    def set_theme(self, theme):
        self.model.set_theme(theme)

    def set_save_folder(self, folder):
        self.model.set_folder(folder)

    def get_save_folder(self):
        return self.model.get_folder()

    def set_user_details_path(self, path):
        self.model.set_user_details(path)

    def get_user_details_path(self):
        return self.model.get_user_details()

    def get_all_settings(self):
        return self.model

    def get_all_settings_by_section(self, section):
        pass

    def get_setting_by_option(self, option):
        # section = self.find_section(option)
        # return self.get_settings_by_id(section, option)
        pass

    def get_setting_by_path(self, path):
        self.read_config(path)
        return self.updater.to_dict()

    def save(self, settings):
        with open(self.model.get_path(), 'w'):
            self.parser.write(settings)

    def config_exists(self):
        return True if Path(self.model.get_path()).exists() else False

    def read_config(self, config_path):
        try:
            with open(config_path, 'r') as config_file:
                self.updater.read_file(config_file)
        except FileNotFoundError as e:
            print(create_error_message(error_type='settings',
                                       message=f'Unable to read {config_path}',
                                       error_message=str(e)))

    def create_initial_settings(self):
        try:
            config_contents = f"""
               [System]        
               Theme = none

               [Files]
               config.ini = {self.model.get_path()}
               save_folder = {Path(self.default_config_path).parent}
               user_details_path = none
               """
            self.updater.read_string(config_contents)
            self.save(self.updater.to_dict())

        except configparser.DuplicateSectionError:
            print('Files Section Already Created')
        except configupdater.NoConfigFileReadError:
            print('Unable read config.ini')
        except configparser.ParsingError:
            print('Unable to write to config.ini')

    def initialise_config_file(self, config_path=None):
        try:
            self.model.set_path(self.default_config_path if config_path is None else config_path)
            if not self.config_exists():
                self.create_initial_settings()
            self.read_config(self.get_config_path())
            return self.model.create_settings_object()
        except FileNotFoundError as e:
            print(create_error_message(error_type='settings',
                                       message=f'Unable to initialise settings path {config_path}',
                                       error_message=str(e)))
