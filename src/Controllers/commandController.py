import re
from src.Models.Commands import commands
from src.Utilities.utilities import create_error_message
from pathlib import Path
import json
from datetime import date
import time


class CommandController:

    def __init__(self):
        self.command = commands.Command(None)
        self.command_list_path = Path('src').resolve().parent\
            .joinpath('data/files/command_list.json').as_posix()

        self.arguments_list_path = Path('src').resolve().parent\
            .joinpath('data/files/command_arguments_list.json').as_posix()

        self.options_list_path = Path('src').resolve()\
            .parent.joinpath('data/files/command_options_list.json').as_posix()

        self.user_list_path = Path('src').resolve()\
            .parent.joinpath('data/files/users.json').as_posix()

        self.permissions_list_path = Path('src').resolve()\
            .parent.joinpath('data/files/permissions.json').as_posix()

    def get_command_paths(self):
        return [self.command_list_path, self.arguments_list_path, self.options_list_path]


    def get_valid_commands(self):
        try:
            command_list = {}
            with open(self.command_list_path) as file:
                command_list.update(json.load(file))
            return command_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain valid commands',
                                        error_message=str(fNfE))


    def get_valid_arguments(self):
        try:
            arguments_list = {}
            with open(self.arguments_list_path) as file:
                arguments_list.update(json.load(file))
            return arguments_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain valid arguments',
                                        error_message=str(fNfE))


    def get_valid_options(self):
        try:
            options_list = {}
            with open(self.options_list_path) as file:
                options_list.update(json.load(file))
            return options_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain valid options',
                                        error_message=str(fNfE))

    def get_user_list(self):
        try:
            users_list = {}
            with open(self.user_list_path) as file:
                users_list.update(json.load(file))
            return users_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain user list',
                                        error_message=str(fNfE))
        
    def get_permissions_list(self):
        try:
            permissionss_list = {}
            with open(self.permissions_list_path) as file:
                permissionss_list.update(json.load(file))
            return permissionss_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain permissions list',
                                        error_message=str(fNfE))
        

    def valid_date_format(self, date_format):
        try:
            date.strftime(date.today(), date_format)
            return True
        except Exception as e:
            print(e)
            return False


    def valid_sleep_format(self, time_format):
        try:
            time.strftime(time.localtime(), time_format)
            return True
        except Exception as e:
            print(e)
            return False


    def parse_command(self, user_defined_command):
        commands_from_file = self.get_valid_commands()
        try:
            for cmd in commands_from_file:
                if cmd == user_defined_command:
                    return cmd, commands_from_file[cmd]
                else:
                    raise IOError
        except IOError as ioe:
            return create_error_message(error_type='parse', message='Valid command not found', error_message=str(ioe))


    def parse_arguments(self, user_defined_arguments):
        command_name = self.command.get_command_name()
        valid_command_arguments = self.get_valid_arguments()
        valid_user_args = None
        try:
            for command_name_file in valid_command_arguments.keys():
                # Check that the command is present in the file
                if command_name == command_name_file:
                    file_arguments = valid_command_arguments[command_name]
                    # Compare the user defined args against the ones from the file
                    for user_args, file_args in zip(user_defined_arguments, file_arguments):
                        for cmd_name in self.get_valid_commands():
                            match cmd_name:
                                case 'help':
                                    if user_args in self.get_valid_commands():
                                        valid_user_args = True
                                case ['clear', 'history', 'uptime', 'pwd', 'shutdown', 'halt', 'reboot', 'top']:
                                    if user_args is None:
                                        valid_user_args = True
                                case 'date':
                                    if self.valid_date_format(user_args):
                                        valid_user_args = True
                                case 'sleep':
                                    if self.valid_sleep_format(user_args):
                                        valid_user_args = True
                                case ['id', 'groups', 'passwd', 'last']:
                                    if user_args in self.get_user_list():
                                        valid_user_args = True
                                case 'who':
                                    if user_args == 'am i':
                                        valid_user_args = True
                                case 'ls':
                                    if Path(user_args).is_dir():
                                        valid_user_args = True
                                case 'cp':
                                    if Path(user_args[0]).exists() and Path(user_args[1]).exists():
                                        valid_user_args = True
                                case ['rm', 'cat', 'more', 'head', 'less', 'tail']:
                                    if Path(user_args).is_file():
                                        valid_user_args = True
                                case 'mv':
                                    if (Path(user_args[0]).is_file() and Path(user_args[1]).is_file()) or\
                                            (Path(user_args[0]).is_file() and Path(user_args[1]).is_dir()):
                                        valid_user_args = True
                                case ['chown', 'chmod']:
                                    if user_args[0] in self.get_permissions_list and \
                                            (Path(user_args[1]).is_file() or Path(user_args[1]).is_file()):
                                        valid_user_args = True
                                case 'grep':
                                    if isinstance(user_args[0], str) and Path(user_args[1]).is_file():
                                        valid_user_args = True
                                case 'ln':
                                    if Path(user_args[0]).is_absolute() and isinstance(user_args[1], str):
                                        valid_user_args = True
                                case ['mkdir', 'rmdir']:
                                    if Path(user_args).is_dir():
                                        valid_user_args = True
                                case 'ps':
                                    if isinstance(user_args, int):
                                        valid_user_args = True
                                case 'kill':
                                    if isinstance(user_args[0], int) and isinstance(user_args[1], int):
                                        valid_user_args = True
                    if valid_user_args:
                        return file_arguments
                    else:
                        raise IOError
        except IOError as ioe:
            return create_error_message(error_type='parse', message=f'Unable to get arguments for {command_name}',
                                        error_message=str(ioe))



    def parse_option(self, user_defined_options):
        try:
            # Get command options dict from file
            command_name = self.command.get_command_name()
            valid_command_options = self.get_valid_options()
            # Get the command name from the dict keys and
            # check that the user selected command is found in the dict
            for command_name_file in valid_command_options.keys():
                if command_name == command_name_file:
                    # if so get the corresponding list of options for the command
                    file_options = valid_command_options[command_name]

                    chosen_options = {'': ''}
                    # for each chosen option get the matching file option
                    for chosen_opt, file_opt in zip(user_defined_options, file_options):
                        # Use regex to check if the option is valid
                        regex = r"(^\A-+)([a-z]$)"
                        matches = re.Match(regex, chosen_opt, re.MULTILINE)
                        if matches:
                            # Check if the option is not available for this command or just has a few options
                            # aka fewer options that the max allowed
                            if chosen_opt == file_opt:
                                chosen_options.update({'Valid option', file_opt})
                            elif chosen_opt != file_opt:
                                chosen_options.update({'Invalid option', file_opt})
                            elif chosen_opt is None:
                                chosen_options.update('No option')


                    # if the number of chosen options exceeds the number of options
                    # from the list then index error raised
                    if len(chosen_options) > len(file_options):
                        raise IndexError

                    no_option = 0
                    valid_option = 0
                    for chosen_opt in chosen_options:
                        match chosen_opt:
                            case 'Invalid option':
                                raise IOError
                            # If chosen_options contains no options or is none then raise IOError
                            case 'No option':
                                no_option += 1
                                if no_option < 1:
                                    raise IOError
                            # If all chosen_options return dict
                            case 'Valid option':
                                valid_option += 1
                                if valid_option == len(chosen_options):
                                    return chosen_options

        except (IOError, IndexError) as e:
            return create_error_message(error_type='parse', message=f'Options {user_defined_options} are not valid',
                                        error_message=str(e))


    def load_command(self, user_defined_command, user_defined_arguments, user_defined_options):
        command, command_type = self.parse_command(user_defined_command)
        self.command.set_command_name(command)
        self.command.set_command_type(command_type)

        arguments = self.parse_arguments(user_defined_arguments)
        self.command.set_command_arguments(arguments)

        options = self.parse_option(user_defined_options)
        self.command.set_command_options(options)








