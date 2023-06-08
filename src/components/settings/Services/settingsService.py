from timeit import default_timer as timer
import logging
import time

import pysnooper
import pytz
import re
from src.components.Utilities.utilities import hash_password


@pysnooper.snoop()
class SettingsService:
    def __init__(self, repo, validator, logger):
        self.repository = repo
        self.validator = validator
        self.object_loaded = None
        self.logger = logger
        self.success = None

    def create_new_settings_obj(self, default_path):
        settings = self.repository.initialise_config_file(default_path)
        self.repository.set_initial_vars()
        self.object_loaded = True
        return settings

    def existing_settings_obj(self, path):
        settings = self.repository.get_settings_by_path(path)
        self.repository.set_initial_vars()
        self.object_loaded = True
        return settings

    def present(self, path):
        path_present = self.validator.path_present(self.object_loaded, path)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Path present: {path_present}')
        return path_present

    def change_current_theme(self, theme):
        return self.repository.set_theme(theme)

    def get_default_theme(self):
        return self.repository.default_theme()

    def get_previous_theme(self):
        return self.repository.get_last_theme()


    def establish_theme(self, new_theme=None):
        previous_theme, current_theme = self.repository.get_themes()
        theme_status = self.validator.theme_status(previous_theme, current_theme, new_theme)
        match theme_status:
            case 'default':
                self.repository.change_theme_order(default=True)
            case 'update_default':
                self.repository.change_theme_order(previous=current_theme, current=new_theme)
            case 'update':
                self.repository.change_theme_order(previous=current_theme, current=new_theme)

        updated_previous_theme, updated_current_theme = self.repository.get_themes()
        return updated_current_theme


    def establish_save_folder(self, new_save_folder):
        save_folder = self.repository.get_save_folder()
        if new_save_folder:
            if self.validator.validate_save_folder(new_save_folder, save_folder):
                self.repository.change_save_folder(new_save_folder)
                return self.repository.create_existing_settings()
        return save_folder

    def establish_timezone(self, new_timezone):
        if new_timezone:
            old_timezone = self.repository.get_timezone()
            if isinstance(new_timezone, str):
                new_timezone = pytz.timezone(new_timezone)
            if self.validator.validate_timezones(old_timezone, new_timezone):
                self.repository.change_timezone(new_timezone)
            return self.repository.create_existing_settings()
        return self.repository.get_timezone()

    def initialise_user(self, username, password):
        #  Create encrypted password, which is a reference to actual password
        hashed_password = hash_password(password)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Encrypted password created for {username}')
        #  Ensure that password references encrypted password not vice versa
        if self.validator.validate_password(password, hashed_password):
            self.logger.create_log_entry(level=logging.DEBUG, message='Password matches encrypted version')
            # If so build a user details object
            user_details = self.repository.create_new_user_details(username, hashed_password)
            self.logger.create_log_entry(level=logging.DEBUG, message=f'New user details object created')
            # Make a reference in the settings ini file
            self.repository.establish_credential_variables(user_details, set_active_user=True)
            # Save the username and encrypted password to the database
            last_entry = self.repository.save_user_details(user_details)
            # check last entry corresponds to defined credentials
            success = self.validator.validate_database_entry(last_entry[0], user_details)
            # password fails to reference encrypted password (system error) inform the logger and exit method
            if not success:
                self.logger.create_log_entry(level=logging.ERROR, message='Unable to initialise user')

            return success
        else:
            self.logger.create_log_entry(level=logging.ERROR, message='Password does not match encrypted password')

    def load_user(self, username, password):
        # User has been identified so query database for user details
        users = self.repository.get_all_users()
        if self.validator.username_in_db(username, users):
            user_details = self.repository.get_user_details(username, password)
            if self.validator.validate_password(password, user_details.get_password()):
                self.repository.establish_credential_variables(user_details, set_active_user=True)
                return self.validator.validate_user_details(username, password, user_details)

    def credential_handling(self, username, password, check_active_user=False):
        if username and check_active_user:
            return self.validator.is_active_user(username, self.repository.get_active_user())

        if username and password:
            if not self.repository.database_exists():
                self.repository.intialise_database(username, password)
                self.logger.create_log_entry(level=logging.CRITICAL, message='Initialising database')
            #  Credentials should have pre-defined format standard
            if self.validator.valid_credential_format(username, password):
                self.success = None
                # If user not found start user creation processes
                user_exists = self.repository.check_user_exists(username)
                self.logger.create_log_entry(level=logging.DEBUG, message=f'Username: {username} found?: {user_exists}')
                if not user_exists:
                    self.success = self.initialise_user(username, password)
                # if user has been initialised or the initialisation process has completed without error
                elif user_exists or self.success is True:
                    return self.load_user(username, password)

            # If fail to match the format, inform the logger and exit method
            if not self.success:
                self.logger.create_log_entry(level=logging.CRITICAL, message='Username or password is invalid')

    def prompt_line_from_settings(self):
        active_user, current_dir = self.repository.get_prompt_line_variables()
        self.repository.set_prompt_line(f"{active_user}|{current_dir}$")
        return self.repository.get_prompt_line()

    def defined_prompt_line(self, prompt_line):
        self.repository.set_prompt_line(prompt_line)
        return self.repository.get_prompt_line()

    def prompt_line_handling(self, prompt_line=None):
        if not prompt_line:
            return self.prompt_line_from_settings()
        return self.defined_prompt_line(prompt_line)

    def normalise_format_string(self, fmt):
        split_fmt = fmt.split(':')
        split_fmt = [ele.split('%') for ele in split_fmt]
        new_fmt = []
        for index in range(len(split_fmt)):
            for token in split_fmt[index]:
                if re.match(r'[a-zA-Z]', token):
                    new_fmt.append(f'%{token}')
        return ':'.join(new_fmt)

    def encode_format_string(self, fmt):
        split_fmt = fmt.split(':')
        new_fmt = []
        for token in split_fmt:
            if token.startswith('%'):
                new_fmt.append(f'%{token}')
        return ':'.join(new_fmt)

    def save_datetime_format(self, fmt):
        parsed_fmt = self.encode_format_string(self.normalise_format_string(fmt))
        self.repository.change_datetime_format(parsed_fmt)
        return f'Datetime format changed to {fmt}'

    def get_current_datetime_format(self):
        format_string = self.repository.get_datetime_format()
        return self.normalise_format_string(format_string)

    def establish_datetime_format(self, fmt=None):
        if not fmt:
            return self.get_current_datetime_format()
        return self.save_datetime_format(fmt)

    def establish_runtime(self, startup=None, current=None):
        if startup:
            self.repository.set_startup_time(timer())
        if current:
            start_time = self.repository.get_startup_time()
            current_time = timer()
            runtime = current_time - float(start_time)
            return f'{int(runtime)} seconds'



