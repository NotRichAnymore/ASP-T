from src.components.Utilities.utilities import create_error_message
import string
import pysnooper


@pysnooper.snoop()
class CommandService:
    def __init__(self, repo, validator):
        self.repository = repo
        self.validator = validator
        self.command_name = None
        self.command_arguments = []
        self.command_options = []

    def get_by_path(self, path):
        return self.repository.get_by_path(path)

    def get_all_paths(self):
        return self.repository.get_all()

    def add_command_argument(self, argument):
        self.command_arguments.append(argument)

    def add_command_option(self, option):
        self.command_options.append(option)

    def establish_command_format(self, command):
        return self.repository.get_command_format(command)

    def determine_command_arguments(self, command, arg_format, tokens):
        match command:
            case 'help':
                for token in tokens:
                    if token in self.repository.get_all_commands():
                        return token

    @staticmethod
    def determine_command_options(command, opt_format, tokens):
        match command:
            case 'help':
                return None

    def determine_command(self, tokens, command_format):
        command = command_format[0]
        command_args = self.determine_command_arguments(command, command_format[1], tokens[1:])
        command_opts = self.determine_command_options(command, command_format[2], tokens[1:])

        return [command, command_args, command_opts]

    def parse(self, command_statement):
        tokens = command_statement.split(' ')
        command_format = self.establish_command_format(tokens[0])
        return self.determine_command(tokens, command_format)

    def run_command(self, command):
        pass


    def command_order(self):
        pass
