import logging

import configupdater
import configparser
import PySimpleGUI as sg
from pathlib import Path
from src.components.Utilities.utilities import create_error_message
from src.components.settings.Models.Settings import Settings
from src.components.settings.Models.User import User
import pysnooper


class SettingsRepository:

    def __init__(self, logger):
        self.model = Settings()
        self.user_model = User()
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

        self.logger = logger

    def get_config_path(self):
        self.logger.create_log_entry(level=logging.DEBUG,
                                     message=f'Getting config path: {self.config_path}')
        return self.config_path

    def get_save_folder(self):
        self.logger.create_log_entry(level=logging.DEBUG,
                                     message=f'Getting save folder: {self.save_folder}')
        return self.save_folder

    def get_user_details_path(self):
        self.logger.create_log_entry(level=logging.DEBUG,
                                     message=f'Getting user details path: {self.user_details_path}')
        return self.user_details_path

    def get_themes(self):
        self.logger.create_log_entry(level=logging.DEBUG,
                                     message=f'Getting Themes: {self.themes}')
        return self.themes

    def get_settings_by_path(self, path):
        self.set_config_path(path)
        self.read_config()
        return sg.UserSettings(filename=path, use_config_file=True, convert_bools_and_none=True)

    def set_inital_config_path(self, path):
        self.logger.create_log_entry(level=logging.DEBUG,
                                     message=f'Setting initial config path as {path}')
        self.config_path = path

    def set_config_path(self, path):
        try:
            self.logger.create_log_entry(
                level=logging.DEBUG, message=f'Setting config path as {path} from {self.config_path}')
            self.read_config()
            self.updater['Files']['config.ini'] = self.get_config_path()
            self.config_path = self.updater['Files']['config.ini']
        except FileNotFoundError as e:
            self.logger.create_log_entry(level=logging.ERROR, message=f'Unable to set {path}'
                                                                      f'Stack Trace: {str(e)}')

    def set_save_folder(self, folder):
        self.logger.create_log_entry(
            level=logging.DEBUG, message=f'Setting save folder as {folder} from {self.save_folder}')
        self.read_config()
        self.updater['Files']['save_folder'] = folder
        self.save_folder = self.updater['Files']['save_folder']

    def set_user_details_path(self, path):
        self.logger.create_log_entry(
            level=logging.DEBUG, message=f'Setting user details path as {path} from {self.user_details_path}')
        self.read_config()
        self.updater['Files']['user_details_path'] = path
        self.user_details_path = self.updater['Files']['user_details_path']

    def set_themes(self, themes):
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Setting theme as {themes} from {self.themes}')
        self.themes = themes

    @pysnooper.snoop()
    def set_initial_vars(self):
        self.logger.create_log_entry(level=logging.DEBUG, message='Setting repository variables')
        themes = (self.updater['System']['previous_theme'].value, self.updater['System']['current_theme'].value)
        self.set_themes(themes)
        self.set_inital_config_path(self.updater['Files']['config.ini'].value)
        self.set_save_folder(self.updater['Files']['save_folder'].value)
        self.set_user_details_path(self.updater['Files']['user_details_path'].value)
        self.logger.create_log_entry(level=logging.DEBUG, message='Repository variables set')

        
    @pysnooper.snoop()
    def change_theme_order(self, previous=None, current=None, default=None):
        self.read_config()
        self.logger.create_log_entry(level=logging.INFO, message='Changing theme order')
        if default:
            self.logger.create_log_entry(level=logging.INFO, message='Default theme order')
            self.updater['System']['previous_theme'] = 'Null'
            self.updater['System']['current_theme'] = 'SystemDefault'
            themes = 'Null', 'SystemDefault'
        else:
            self.logger.create_log_entry(level=logging.INFO, message='Changing themes from '
                                                                     f"{self.updater['System']['previous_theme']}"
                                                                     f" and {self.updater['System']['current_theme']} "
                                                                     f"to {previous} and {current}")
            self.updater['System']['previous_theme'] = previous
            self.updater['System']['current_theme'] = current
            themes = previous, current
        self.write_to_config()
        self.set_themes(themes)
        self.logger.create_log_entry(level=logging.INFO, message='Theme order changed')


    @pysnooper.snoop()
    def change_save_folder(self, save_folder):
        self.read_config()
        self.logger.create_log_entry(
            level=logging.INFO,
            message=f"Changing save folder from {self.updater['Files']['save_folder']} to {save_folder}")
        self.updater['Files']['save_folder'] = save_folder
        self.write_to_config()
        self.set_save_folder(save_folder)
        self.logger.create_log_entry(level=logging.INFO, message='Save folder changed')

    @pysnooper.snoop()
    def create_existing_settings(self):
        self.read_config()
        self.logger.create_log_entry(level=logging.INFO, message=f'Creating existing settings from {self.config_path}')
        return sg.UserSettings(filename=self.config_path, use_config_file=True, convert_bools_and_none=True)

    def config_exists(self, config_path=None):
        self.logger.create_log_entry(level=logging.INFO, message=f'Checking {config_path} exists')
        if not config_path:
            path = self.get_config_path()
            if path is None:
                self.logger.create_log_entry(level=logging.INFO, message=f'{config_path} does not exist')
                return False
            self.logger.create_log_entry(level=logging.INFO, message=f'{config_path} exists {Path(path).exists()}')
            return True if Path(path).exists() else False
        self.logger.create_log_entry(level=logging.INFO, message=f'{config_path} exists {Path(config_path).exists()}')
        return True if Path(config_path).exists() else False

    def read_config(self):
        try:
            with open(self.get_config_path(), 'r') as config_file:
                self.updater.read_file(config_file)
        except FileNotFoundError as e:
            self.logger.create_log_entry(level=logging.ERROR, message=f'Unable to read {self.get_config_path()}.'
                                                                      f'Stack Trace: {str(e)}')

    def write_to_config(self):
        try:
            self.logger.create_log_entry(level=logging.INFO, message=f'Writing to {self.get_config_path()}')
            with open(self.get_config_path(), 'w') as config_file:
                self.updater.write(config_file)
        except Exception as e:
            self.logger.create_log_entry(level=logging.ERROR, message=f'Unable to write to {self.get_config_path()}.'
                                                                      f'Stack Trace: {str(e)}')

    def load_updater(self, config_contents):
        self.updater.read_string(config_contents)
        self.logger.create_log_entry(level=logging.INFO, message='Loading updater with settings contents')

    @pysnooper.snoop()
    def create_initial_settings(self):
        try:
            self.logger.create_log_entry(level=logging.INFO, message='Filling settings contents')
            config_contents = f"""
                [System]
                previous_theme = Null
                current_theme = SystemDefault

                [Files]
                config.ini = {self.config_path}
                save_folder = {self.default_save_folder}
                user_details_path = {self.default_user_details_path}
                
                [Users]
                guest
                """
            self.load_updater(config_contents)
            self.logger.create_log_entry(level=logging.INFO, message=f'Reading from {self.config_path}')
            self.parser.read_string(config_contents)
            self.logger.create_log_entry(level=logging.INFO, message=f'Writing to {self.config_path}')
            with open(self.config_path, 'w') as config_file:
                self.parser.write(config_file)
            self.logger.create_log_entry(level=logging.CRITICAL, message='New Settings Created')
            return sg.UserSettings(filename=self.config_path, use_config_file=True, convert_bools_and_none=True)

        except (configparser.DuplicateSectionError,
                configupdater.NoConfigFileReadError,
                configparser.ParsingError) as e:
            self.logger.create_log_entry(level=logging.ERROR, message=f'Unable to create initial settings, Stack Trace:{str(e)}')

    @pysnooper.snoop()
    def initialise_config_file(self, default_path, config_path=None):
        default_config_path = Path(self.default_config_path).as_posix()
        try:
            if default_path:
                self.logger.create_log_entry(level=logging.CRITICAL, message='Using default path')
                self.set_inital_config_path(default_config_path)
                if not self.config_exists(default_config_path):
                    self.logger.create_log_entry(level=logging.CRITICAL, message='Initialising ini file')
                    return self.create_initial_settings()
                self.logger.create_log_entry(level=logging.CRITICAL, message='Default Path already present')
                self.read_config()
                return self.create_existing_settings()

            if config_path:
                if not self.config_exists(config_path):
                    raise FileNotFoundError
                self.set_inital_config_path(config_path)
                self.read_config()
                return self.create_existing_settings()

        except FileNotFoundError:
            self.logger.create_log_entry(level=logging.ERROR, message='Config path not found')
            self.logger.create_log_entry(level=logging.ERROR, message='Using default path instead')
            self.set_inital_config_path(default_config_path)
            return self.create_initial_settings()

    def create_new_user_details(self, username, hashed_password):
        return self.user_model.create_user_details(username, hashed_password)

    def establish_credential_variables(self, user_details):
        self.read_config()
        self.updater['Users']['guest'].add_after.option(key=user_details.get_username())
        self.write_to_config()

    def save_user_details(self, user_details):
        pass

    def get_all_users(self):
        pass

    def get_user_details(self, username, password):
        pass
