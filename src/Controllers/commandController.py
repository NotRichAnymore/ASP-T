import re
from src.Models.Commands import commands
from src.Utilities.utilities import create_error_message
import json


class CommandController:

    def __init__(self):
        self.command = commands.Command(None)

    @staticmethod
    def get_valid_commands():
        try:
            command_list = {}
            with open('src/Files/command_list.json') as file:
                command_list.update(json.load(file))
            return command_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain valid commands',
                                        error_message=str(fNfE))

    @staticmethod
    def get_valid_options():
        try:
            options_list = {}
            with open(f'src/Files/command_options_list.json') as file:
                options_list.update(json.load(file))
            return options_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain valid options',
                                        error_message=str(fNfE))

    def parse_command(self, user_defined_command):
        commands_from_file = self.get_valid_commands()
        try:
            for cmd in commands_from_file:
                if cmd == user_defined_command:
                    self.command.set_command_name(cmd)
                else:
                    raise IOError
        except IOError as ioe:
            return create_error_message(error_type='parse', message='Valid command not found', error_message=str(ioe))

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

        except (IOError, IndexError) as (ioe, ine):
            return create_error_message(error_type='parse', message=f'Options {user_defined_options} are not valid',
                                        error_message=str(ioe))
