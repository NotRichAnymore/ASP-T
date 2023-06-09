import base64
import logging
import re
from pathlib import Path

import bcrypt
import pysnooper


@pysnooper.snoop()
class SettingsValidator:
    def __init__(self, logger):
        self.logger = logger

    def path_present(self, object_loaded, path=None):
        if path:
            return Path(path).exists()
        return False if not object_loaded or object_loaded is None else True

    def theme_status(self, previous_theme, current_theme, new_theme):
        if previous_theme is None and current_theme is None and \
                new_theme == 'SystemDefault' or new_theme == 'Default' or new_theme is None:
            self.logger.create_log_entry(level=logging.DEBUG, message='Using Default Themes')
            return 'default'
        if previous_theme is None and current_theme == 'SystemDefault':
            self.logger.create_log_entry(level=logging.DEBUG, message='Updating Default Themes')
            return 'update_default'
        if current_theme and previous_theme and new_theme:
            self.logger.create_log_entry(
                level=logging.DEBUG, message=f'Updating Themes from {current_theme} to {new_theme}')
            return 'update'

    def validate_save_folder(self, new_save_folder, old_save_folder):
        if new_save_folder != old_save_folder and Path(new_save_folder).exists():
            self.logger.create_log_entry(level=logging.DEBUG, message=f'New save folder: {new_save_folder} valid')
            return True
        self.logger.create_log_entry(level=logging.DEBUG, message=f'New save folder {new_save_folder} not valid')
        return False

    def validate_timezones(self, old_timezone, new_timezone):
        return True if old_timezone.zone != new_timezone.zone else False

    @staticmethod
    @pysnooper.snoop()
    def validate_username(expected, actual):
        return True if expected == actual else False


    @staticmethod
    @pysnooper.snoop()
    def username_in_db(username, users):
        for index in range(len(users)):
            if username in users[index][0]:
                return True
        return False

    @staticmethod
    @pysnooper.snoop()
    def validate_password(password, hashed_password):
        if not isinstance(password, bytes) :
            password = base64.b64encode(bytes(password, 'utf-8'))
        if not isinstance(hashed_password, bytes):
            hashed_password = bytes(hashed_password, 'utf-8')
        return bcrypt.checkpw(password, hashed_password)

    def validate_user_details(self, username, password, user_details):
        if self.validate_username(username, user_details.get_username()) \
                and self.validate_password(password, user_details.get_password()):
            return True
        return False

    def valid_credential_format(self, username, password):
        # regex check for 8+ latin chars, no special chars outside standard nums and symbols
        # regex check for 8+ latin chars, 2 numbers, 1 symbol
        # if u and p both pass return true else false and let logger know which failed.
        username_format = r"^([a-z|A-Z|\u00C0-\u00FF]{8,16})$"
        password_format = r"(((?=\S*[A-Z])(?=\S*[a-z])(?=\S*\d)(?=\S*[\!\"\£\$\%\^&\*\(\)?\_\~\@\:\;\<\>\/\[\]\\])\S{8,16}))"
        if re.match(username_format, username) and re.match(password_format, password):
            self.logger.create_log_entry(level=logging.CRITICAL, message='Username and Password format is valid')
            return True
        return False

    def validate_database_entry(self, database_entry, user_details):
        if (user_details.get_username() == database_entry[0]) and \
                (user_details.get_password() == bytes(database_entry[1], 'utf-8')):
            return True
        return False

    def is_active_user(self, username, active_user):
        if username == active_user:
            return True
        return False
