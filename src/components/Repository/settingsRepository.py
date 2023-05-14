import configupdater
import configparser
import PySimpleGUI as sg
from pathlib import Path
from src.components.Utilities.utilities import create_error_message
from src.components.Models.Settings import Settings
import pysnooper


class SettingsRepository:

    def __init__(self):
        self.model = Settings()
        self.updater = configupdater.ConfigUpdater()
        self.parser = configparser.ConfigParser()
        self.default_save_folder = Path('src').resolve().parent.parent\
            .joinpath('data/files').as_posix()
        self.save_folder = None

        self.default_config_path = Path('src').resolve().parent.parent.joinpath('data/files/config.ini').as_posix()
        self.config_path = None

        self.default_user_details_path = None
        self.user_details_path = None

        self.default_themes = None, None
        self.themes = None, None

    def get_config_path(self):
        return self.config_path

    def get_save_folder(self):
        return self.save_folder

    def get_user_details_path(self):
        return self.user_details_path

    def get_themes(self):
        return self.themes

    def get_settings_by_path(self, path):
        self.set_config_path(path)
        self.read_config()
        return sg.UserSettings(filename=path, use_config_file=True, convert_bools_and_none=True)

    def set_inital_config_path(self, path):
        self.config_path = path

    def set_config_path(self, path):
        try:
            self.read_config()
            self.updater['Files']['config.ini'] = self.get_config_path()
            self.config_path = self.updater['Files']['config.ini']
        except FileNotFoundError as e:
            return create_error_message(error_type='settings',
                                        message=f'Unable to read {path}',
                                        error_message=str(e))

    def set_save_folder(self, folder):
        self.read_config()
        self.updater['Files']['save_folder'] = folder
        self.save_folder = self.updater['Files']['save_folder']

    def set_user_details_path(self, path):
        self.read_config()
        self.updater['Files']['user_details_path'] = path
        self.user_details_path = self.updater['Files']['user_details_path']

    def set_themes(self, themes):
        self.themes = themes

    @pysnooper.snoop()
    def set_initial_vars(self):
        themes = (self.updater['System']['previous_theme'].value, self.updater['System']['current_theme'].value)
        self.set_themes(themes)

        self.set_inital_config_path(self.updater['Files']['config.ini'].value)
        self.set_save_folder(self.updater['Files']['save_folder'].value)
        self.set_user_details_path(self.updater['Files']['user_details_path'].value)
        
        
    @pysnooper.snoop()
    def change_theme_order(self, previous=None, current=None, default=None):
        self.read_config()
        if default:
            self.updater['System']['previous_theme'] = 'Null'
            self.updater['System']['current_theme'] = 'SystemDefault'
            themes = 'Null', 'SystemDefault'
        else:
            self.updater['System']['previous_theme'] = previous
            self.updater['System']['current_theme'] = current
            themes = previous, current
        self.write_to_config()


        self.set_themes(themes)


    @pysnooper.snoop()
    def create_existing_settings(self):
        self.read_config()
        return sg.UserSettings(filename=self.config_path, use_config_file=True, convert_bools_and_none=True)

    def config_exists(self, config_path=None):
        if not config_path:
            path = self.get_config_path()
            if path is None:
                return False
            return True if Path(path).exists() else False
        return True if Path(config_path).exists() else False

    def read_config(self):
        try:
            with open(self.get_config_path(), 'r') as config_file:
                self.updater.read_file(config_file)
        except FileNotFoundError as e:
            return create_error_message(error_type='settings',
                                        message=f'Unable to read {self.get_config_path()}',
                                        error_message=str(e))

    def write_to_config(self):
        try:
            with open(self.get_config_path(), 'w') as config_file:
                self.updater.write(config_file)
        except Exception as e:
            return create_error_message(error_type='settings',
                                        message=f'Unable to read {self.get_config_path()}',
                                        error_message=str(e))

    def load_updater(self, config_contents):
        self.updater.read_string(config_contents)

    @pysnooper.snoop()
    def create_initial_settings(self):
        try:
            config_contents = f"""
                [System]
                previous_theme = Null
                current_theme = SystemDefault

                [Files]
                config.ini = {self.config_path}
                save_folder = {self.default_save_folder}
                user_details_path = {self.default_user_details_path}
                """
            self.load_updater(config_contents)
            self.parser.read_string(config_contents)
            with open(self.config_path, 'w') as config_file:
                self.parser.write(config_file)
            return sg.UserSettings(filename=self.config_path, use_config_file=True, convert_bools_and_none=True)

        except (configparser.DuplicateSectionError,
                configupdater.NoConfigFileReadError,
                configparser.ParsingError) as e:
            return create_error_message(error_type='settings',
                                        message='Unable to create initial settings',
                                        error_message=str(e))

    @pysnooper.snoop()
    def initialise_config_file(self, default_path, config_path=None):
        default_config_path = Path(self.default_config_path).as_posix()
        try:
            if default_path:

                self.set_inital_config_path(default_config_path)
                if not self.config_exists(default_config_path):
                    return self.create_initial_settings()
                self.read_config()
                return self.create_existing_settings()

            if config_path:
                if not self.config_exists(config_path):
                    raise FileNotFoundError
                self.set_inital_config_path(config_path)
                self.read_config()
                return self.create_existing_settings()

        except FileNotFoundError:
            self.set_inital_config_path(default_config_path)
            return self.create_initial_settings()



            # return create_error_message(error_type='settings',
            #                            message=f'Unable to initialise settings path {config_path}',
            #                            error_message=str(e))
