import logging


import pysnooper


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

    @pysnooper.snoop()
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

    @pysnooper.snoop()
    def establish_save_folder(self, new_save_folder):
        save_folder = self.repository.get_save_folder()
        if self.repository.validate.save_folder(new_save_folder, save_folder):
            self.repository.change_save_folder(new_save_folder)
            return self.repository.create_existing_settings()

    def initialise_user(self, username, password):
        #  Create encrypted password, which is a reference to actual password
        internal_password = self.create_encrypted_password(password)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Encrypted password created for {username}')
        #  Ensure that password references encrypted password not vice versa
        if self.validator.validate_password(password, internal_password):
            # If so build a user details object
            user_details = self.repository.create_new_user_details(username, password, internal_password)
            self.logger.create_log_entry(level=logging.DEBUG,
                                         message=f'New user details object created: {user_details}')
            # Make a reference in the settings ini file
            self.repository.establish_credential_variables(user_details)
            self.logger.create_log_entry(level=logging.DEBUG, message=f'Added user:{username} to settings.ini')
            # Save the username and encrypted password to the database
            success = self.repository.save_user_details(user_details)
            return success
        # password fails to reference encrypted password (system error) inform the logger and exit method
        self.logger.create_log_entry(level=logging.ERROR, message=f'Failure to encrypt password for {username}')

    def load_user(self, username, password):
        # User has been identified so query database for user details
        users = self.repository.get_all_users()
        if self.validator.validate_username(username, users):
            user_details = self.repository.get_user_details(username, password)
            self.repository.establish_credential_variables(user_details)
            return self.validator.validate_credentials(user_details)

    def credential_handling(self, username, password):
        #  Credentials should have pre-defined format standard
        if self.validator.valid_credential_format(username, password):
            # If user not found start user creation processes
            if not self.validator.check_user_exist(username):
                self.logger.create_log_entry(level=logging.DEBUG, message=f'Username: {username} found?: False')
                return self.initialise_user(username, password)

            self.logger.create_log_entry(level=logging.DEBUG, message=f'Username: {username} found?: True')
            return self.load_user(username, password)

        # If fail to match the format, inform the logger and exit method
        self.logger.create_log_entry(level=logging.CRITICAL, message='Username or password is invalid')

