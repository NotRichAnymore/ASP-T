import json
from src.Utilities.utilities import create_error_message


class Command:
    def __init__(self, cmd_name, args):
        self.command_name = cmd_name
        self.arguments = args

    def set_command_name(self, cmd_name):
        self.command_name = cmd_name

    def get_command_name(self):
        return self.command_name

    def set_command_arguments(self, args):
        self.arguments = args

    def get_command_arguments(self):
        return self.arguments

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
    def get_valid_arguments(command_name):
        try:
            arguments_list = {}
            with open(f'src/Files/{command_name}_arguments_list.json') as file:
                arguments_list.update(json.load(file))
            return arguments_list
        except FileNotFoundError as fNfE:
            return create_error_message(error_type='file', message='Unable to obtain valid arguments',
                                        error_message=str(fNfE))
