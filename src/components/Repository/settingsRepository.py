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
        current_theme, previous_themes = themes
        self.read_config()
        self.updater['System']['Current_Theme'] = current_theme
        self.updater['System']['Previous_Theme'] = previous_themes
        self.themes = (self.updater['System']['Current_Theme'], self.updater['System']['Previous_Theme'])

    def change_theme_order(self, previous, current, default=None):
        self.read_config()
        if default:
            self.updater['System']['Previous_Theme'] = 'none'
            self.updater['System']['Current_Theme'] = 'SystemDefault'
        else:
            self.updater['System']['Previous_Theme'] = previous
            self.updater['System']['Current_Theme'] = current

        self.updater.update_file(True)

    @pysnooper.snoop()
    def create_settings(self):
        self.read_config()
        return sg.UserSettings(filename=self.get_config_path(), use_config_file=True, convert_bools_and_none=True)

    def update_settings(self, settings):
        self.config_path, self.save_folder, self.user_details_path, self.themes = settings
        self.set_config_path(self.config_path)
        self.save_folder(self.user_details_path)
        self.user_details_path(self.user_details_path)
        self.set_themes(self.themes)

    def config_exists(self):
        path = self.get_config_path()
        if path is None:
            return False
        return True if Path(path).exists() else False

    def read_config(self):
        try:
            with open(self.get_config_path(), 'r') as config_file:
                self.updater.read_file(config_file)
        except FileNotFoundError as e:
            return create_error_message(error_type='settings',
                                        message=f'Unable to read {self.get_config_path()}',
                                        error_message=str(e))

    @pysnooper.snoop()
    def create_initial_settings(self):
        try:
            previous_theme, current_theme = self.get_themes()
            config_contents = \
                f"""
                [System]
                Previous_Theme = {previous_theme}
                Current_Theme = {current_theme}

                [Files]
                config.ini = {self.config_path}
                save_folder = {self.default_save_folder}
                user_details_path = {self.default_user_details_path}
                """
            self.updater.read_string(config_contents)
            with open(self.config_path, 'w') as config_file:
                self.updater.write(config_file)
            return sg.UserSettings(filename=self.config_path, use_config_file=True, convert_bools_and_none=True)

        except (configparser.DuplicateSectionError,
                configupdater.NoConfigFileReadError,
                configparser.ParsingError) as e:
            return create_error_message(error_type='settings',
                                        message='Unable to create initial settings',
                                        error_message=str(e))

    @pysnooper.snoop()
    def initialise_config_file(self, config_path=None):
        try:
            default_config_path = Path(self.default_config_path).as_posix()
            self.set_inital_config_path(default_config_path)
            if not self.config_exists():
                return self.create_initial_settings()
            self.read_config()
            return self.create_settings()
        except FileNotFoundError as e:
            return create_error_message(error_type='settings',
                                        message=f'Unable to initialise settings path {config_path}',
                                        error_message=str(e))
