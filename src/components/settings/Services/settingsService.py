import logging
import pysnooper
from src.components.Utilities.utilities import hash_password


@pysnooper.snoop()
class SettingsService:
    def __init__(self, repo, validator, logger):
        self.repository = repo
        self.validator = validator
        self.object_loaded = None
        self.logger = logger

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
        if self.repository.validate.save_folder(new_save_folder, save_folder):
            self.repository.change_save_folder(new_save_folder)
            return self.repository.create_existing_settings()


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
            self.repository.establish_credential_variables(user_details)
            # Save the username and encrypted password to the database
            last_entry = self.repository.save_user_details(user_details)
            # check last entry corresponds to defined credentails
            success = self.validator.validate_database_entry(last_entry[0], user_details)
            return success, 'New User'
        # password fails to reference encrypted password (system error) inform the logger and exit method
        self.logger.create_log_entry(level=logging.ERROR, message=f'Password does not match encrypted password')

    def load_user(self, username, password):
        # User has been identified so query database for user details
        users = self.repository.get_all_users()
        if self.validator.validate_username(username, users):
            user_details = self.repository.get_user_details(username, password)
            if self.validator.validate_password(password, user_details.get_password()):
                self.repository.establish_credential_variables(user_details)
                return True if user_details.get_username() == username else False, 'Login User'

    def credential_handling(self, username, password):
        if not self.repository.database_exists():
            self.repository.intialise_database(username, password)
            self.logger.create_log_entry(level=logging.CRITICAL, message='Initialising database')
        #  Credentials should have pre-defined format standard
        if self.validator.valid_credential_format(username, password):
            # If user not found start user creation processes
            if not self.repository.check_user_exists(username):
                self.logger.create_log_entry(level=logging.DEBUG, message=f'Username: {username} found?: False')
                return self.initialise_user(username, password)

            self.logger.create_log_entry(level=logging.DEBUG, message=f'Username: {username} found?: True')
            return self.load_user(username, password)

        # If fail to match the format, inform the logger and exit method
        self.logger.create_log_entry(level=logging.CRITICAL, message='Username or password is invalid')

