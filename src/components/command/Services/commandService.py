import logging

from src.components.command.exceptions import InvalidCommandFormatError
from src.components.Utilities.mySQLUtilities import MySQLUtilities
from mysql.connector import Error
import pysnooper
import re
from pathlib import Path

@pysnooper.snoop()
class CommandService:
    def __init__(self, repo, validator, logger):
        self.repository = repo
        self.validator = validator
        self.logger = logger
        self.command_name = None
        self.command_args = []
        self.command_opts = []
        self.command = []
        self.command_format = None
        self.datetime_format = None
        self.sql = None

    def establish_command_format(self, command):
        return self.repository.get_command_format(command)

    def determine_command_arguments(self, command, arg_format, tokens):
        match command:
            case 'help':
                for token in tokens:
                    if token in self.repository.get_all_commands():
                        return token
            case 'clear':
                return None
            case 'history':
                return None
            case 'date':
                return None
            case 'sleep':
                return tokens
            case 'uptime':
                return None
            case 'id':
                try:
                    self.sql = MySQLUtilities(host='127.0.0.1',
                                              username='test_user',
                                              password='test_pass763',
                                              database='aspt')
                except Exception:
                    return 'unable to check id'
                for token in tokens:
                    ids = self.sql.get_all_users_ids()
                    users = self.sql.get_all_users()
                    for i in range(len(ids)):
                        if int(token) == ids[i][0] or token == users[i][0]:
                            return token
            case 'passwd':
                try:
                    self.sql = MySQLUtilities(host='127.0.0.1',
                                              username='test_user',
                                              password='test_pass763',
                                              database='aspt')
                except Exception:
                    return 'unable to change password'
                username_valid = False
                password_valid = False
                max_length = False
                user_details = []
                users = self.sql.get_all_users()
                users_length = len(users)
                while not max_length or not (username_valid and password_valid):
                    for token in tokens:
                        for i in range(users_length):
                            if i == users_length:
                                max_length = True
                                break

                            if token in users[i][0]:
                                user_details.append(token)
                                username_valid = True

                            if username_valid:
                                try:
                                    password = self.sql.query_user_details(user_details)[2][0]
                                    if self.validator.validate_password(token, password):
                                        user_details.append(token)
                                        password_valid = True
                                except Error:
                                    continue

                        if len(user_details) == 2:
                            username_valid, password_valid = True, True
                            break
                        else:
                            continue

                return user_details if len(user_details) == 2 else None
            case 'ls':
                for token in tokens:
                    if self.validator.validate_path(token):
                        return token



    @staticmethod
    @pysnooper.snoop()
    def determine_command_options(command, opt_format, tokens):
        options = []
        match command:
            case 'help':
                pass
            case 'clear':
                return None
            case 'history':
                return None
            case 'date':
                if len(tokens) == 0:
                    return None
                for token in tokens:
                    if token in opt_format:
                        options.append(token)
                return options
            case 'sleep':
                return None
            case 'uptime':
                return None
            case 'id':
                if len(tokens) == 0:
                    return None
                for token in tokens:
                    if token in opt_format:
                        options.append(token)
                return options
            case 'passwd':
                return None
            case 'ls':
                for token in tokens:
                    if token in opt_format:
                        options.append(token)
                return options

    def help_command(self):
        jsonObject = self.repository.get_all_help_command_details()
        jsonObj = self.repository.get_all_command_details()
        for index in range(len(jsonObject)):
            help_command_details = jsonObject[index]
            command_details = jsonObj[index]
            if self.command_args == help_command_details['name'] and self.command_args in command_details['name'] \
                    and self.command_opts is None:
                response = f"Command Name: {help_command_details['name']}\n" \
                           f"Description: {help_command_details['description']}\n" \
                           f"Arguments: {command_details['arguments']}\n" \
                           f"Options: {command_details['options']}\n" \
                           f"Description: {help_command_details['options']}\n"

                return response

    def clear_command(self):
        return self.command_name

    def history_command(self):
        return self.command_name

    def date_command(self, additional_details):
        timezone, format_string = additional_details[:2]
        if len(self.command) == 1:
            return self.repository.get_current_datetime(timezone, format_string)

        if '-u' in self.command_opts:
            match self.command_opts:
                case ['-u']:
                    return self.repository.get_global_datetimes(format_string)
                case ['-u', '--format=']:
                    if self.validator.validate_date_format((self.command_name, self.command_format),
                                                           self.datetime_format):
                        return self.repository.get_global_datetimes(self.datetime_format)

        if '--format=' in self.command_opts and \
                self.validator.validate_date_format((self.command_name, self.command_format), self.datetime_format):
            match self.command_opts:
                case ['--format=']:
                    return self.repository.get_current_datetime(timezone, self.datetime_format)
                case ['--format=', '-s']:
                    return self.repository.set_datetime_format(self.datetime_format)
        if '--Set=' or '-s' in self.command_opts:
            if self.validator.validate_date_format((self.command_name, self.command_format), self.datetime_format):
                match self.command_opts:
                    case ['--Set=']:
                        return self.repository.set_datetime_format(self.datetime_format)
                    case ['-s']:
                        return self.repository.set_datetime_format(self.datetime_format)

        return InvalidCommandFormatError(self.command_name, self.command_format)

    def ls_command(self):
        directory_contents = None
        if len(self.command_opts) == 0:
            directory_contents = self.repository.get_directory_contents(self.command_args)

        match self.command_opts:
            case ['-a']:
                directory_contents = self.repository.get_directory_contents(self.command_args, show_hidden=True)
            case ['-l']:
                directory_contents = self.repository.get_directory_contents(self.command_args, directory_details=True)
            case ['-d']:
                directory_contents = self.repository.get_directory_contents(self.command_args, only_directory=True)
            case ['-t']:
                directory_contents = self.repository.get_directory_contents(self.command_args, modification_date=True)
            case ['-r']:
                directory_contents = self.repository.get_directory_contents(self.command_args, in_reverse=True)

        return self.command_name, directory_contents

    def sleep_command(self):
        return self.command_name, self.command_args

    def uptime_command(self, additional_details):
        current_time = additional_details[2]
        return current_time

    def id_command(self):
        if len(self.command) == 1:
            return self.command_name

        name_and_id = self.sql.get_usernames_and_ids()
        for i in range(len(name_and_id)):
            for uid in name_and_id:
                if self.command_args in uid:
                    match uid.index(self.command_args):
                        case 0:
                            return self.sql.get_username_by_id(uid[uid.index(self.command_args)])[0][0]
                        case 1:
                            return self.sql.get_id_by_username(uid[uid.index(self.command_args)])[0][0]
        return 'id not found'

    def passwd_command(self, additional_details):
        if not self.command_args[0] == additional_details[3]:
            return None
        return self.command_name, self.command_args

    @staticmethod
    @pysnooper.snoop()
    def set_variable_splitter(variable, datestr, lst):
        variable = re.sub(variable, '', datestr)
        opt = re.sub(variable, '', datestr)
        index = lst.index(datestr)
        lst.remove(datestr)
        lst.insert(index, opt)
        return variable, lst

    def remove_none_values(self):
        command = []
        for ele in self.command:
            if (isinstance(ele, str) and ele is not None) or (isinstance(ele, list) and len(ele) > 0):
                command.append(ele)
        self.command = command

    def additional_requirements(self):
        match self.command_name:
            case 'date':
                self.remove_none_values()
                return True
            case 'uptime':
                return True
            case 'passwd':
                return True
        return False

    def sort_datetime_format(self, tokens):
        for token in tokens:
            if token.startswith('--format='):
                self.datetime_format, tokens = self.set_variable_splitter('--format=', token, tokens)
            if token.startswith('--Set='):
                self.datetime_format, tokens = self.set_variable_splitter('--Set=', token, tokens)

    @staticmethod
    @pysnooper.snoop()
    def sort_path(tokens, opt_format):
        occurance = 0
        start = 0
        end = 0

        quote_present = False
        for token in tokens:
            if "'" in token:
                quote_present = True

        if quote_present:
            for token in tokens:
                occurance += 1
                if occurance == 1:
                    start += tokens.index(token)
                elif occurance == 2:
                    end += tokens.index(token)

            command = tokens[0]
            path = [command] + [' '.join(tokens[start:end])[1:-1]]
            for token in tokens:
                if token in opt_format:
                    path += [token]
            return path

        return tokens

    def build(self, tokens):
        self.command_args = self.determine_command_arguments(self.command_name, self.command_format[1], tokens[1:])
        self.command_opts = self.determine_command_options(self.command_name, self.command_format[2], tokens[1:])
        self.command = [self.command_name, self.command_args, self.command_opts]

    def parse(self, tokens):
        self.command_format = self.establish_command_format(tokens[0])
        self.command_name = self.command_format[0]
        match self.command_name:
            case 'date':
                self.sort_datetime_format(tokens)
            case 'ls':
                tokens = self.sort_path(tokens, self.command_format[2])
        self.validator.validate_command(tokens, self.command_name, self.command_format)
        self.build(tokens)
        return self.additional_requirements()

    def execute_command(self, additional_details=None):
        match self.command_name:
            case 'help':
                return self.help_command()
            case 'clear':
                return self.clear_command()
            case 'history':
                return self.history_command()
            case 'date':
                self.remove_none_values()
                return self.date_command(additional_details)
            case 'sleep':
                return self.sleep_command()
            case 'uptime':
                return self.uptime_command(additional_details)
            case 'id':
                self.remove_none_values()
                return self.id_command()
            case 'passwd':
                return self.passwd_command(additional_details)
            case 'ls':
                return self.ls_command()

    def run_command(self, command_statement, additional_details):
        if not self.parse(command_statement.split(' ')):
            return self.execute_command()
        return self.execute_command(additional_details)

    def write_command_response(self, save_folder, command_response=None, clear_file=None):
        save_path = Path(save_folder).joinpath('command_history.json')
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Using {save_path}')



        jsonObj = self.read_command_history(save_folder)
        mode = 'a+'
        if clear_file:
            self.repository.clear_file(save_path)
            self.repository.write_json_object_to_file(save_path, 'w+', command_response)
        else:
            if len(jsonObj[0]) == 0:
                self.repository.write_json_object_to_file(save_path, mode, command_response)
            self.repository.append_json_object_to_file(save_path, command_response)
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Command Response written to {save_path}')

    def read_command_history(self, save_folder):
        save_path = Path(save_folder).joinpath('command_history.json')
        self.logger.create_log_entry(level=logging.DEBUG, message=f'Reading from {save_path}')
        return self.repository.read_json_object_from_file(save_path)
