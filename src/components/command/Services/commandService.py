from src.components.command.exceptions import InvalidCommandFormatError
import string
import pysnooper


@pysnooper.snoop()
class CommandService:
    def __init__(self, repo, validator):
        self.repository = repo
        self.validator = validator
        self.command_name = None
        self.command_args = []
        self.command_opts = []
        self.command = []
        self.command_format = None


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
            case 'clear':
                return None
            case 'history':
                return None
            case 'date':
                arguments = []
                for token in tokens:
                    if token in self.repository.get__all_datetime_formats() and \
                            self.validator.validate_date_format(token):
                        arguments.append(token)
                    return arguments


    @staticmethod
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
                for token in tokens:
                    if token in opt_format:
                        options.append(token)
                return options

    def determine_command(self, tokens, command_format):
        self.command_name = command_format[0]
        match self.command_name:
            case 'help':
                if len(tokens) != 2:
                    raise InvalidCommandFormatError(self.command_name, command_format)

        self.command_args = self.determine_command_arguments(self.command_name, command_format[1], tokens[1:])
        self.command_opts = self.determine_command_options(self.command_name, command_format[2], tokens[1:])
        self.command = [self.command_name, self.command_args, self.command_opts]


    def parse(self, command_statement):
        tokens = command_statement.split(' ')
        self.command_format = self.establish_command_format(tokens[0])
        self.determine_command(tokens, self.command_format)


    def help_command(self):
        jsonObject = self.repository.get_all_help_command_details()
        for index in range(len(jsonObject)):
            help_command_details = jsonObject[index]
            if self.command_args == help_command_details['name'] and self.command_opts is None:
                response = f"Command Name: {help_command_details['name']}\n" \
                           f"Arguments: {help_command_details['arguments']}\n" \
                           f"Options: {help_command_details['options']}\n" \
                           f"Description: {help_command_details['description']}"
                return response

    def clear_command(self):
        return self.command_name


    def run_command(self):
        match self.command_name:
            case 'help':
                return self.help_command()
            case 'clear':
                return self.clear_command()

    def command_order(self):
        pass
