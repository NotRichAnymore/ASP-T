from src.components.command.exceptions import InvalidCommandFormatError
import pysnooper
import re

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
        self.datetime_format = None

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
        pass

    def date_command(self, additional_parameters):
        timezone, format_string = additional_parameters
        if len(self.command) == 1:
            return self.repository.get_current_datetime(timezone, format_string)

        if '-u' in self.command_opts:
            match self.command_opts:
                case ['-u']:
                    return self.repository.get_global_datetimes(format_string)
                case ['-u', '--format=']:
                    if self.validator.validate_date_format(self.command_name, self.datetime_format):
                        return self.repository.get_global_datetimes(self.datetime_format)

        if '--format=' in self.command_opts and \
                self.validator.validate_date_format(self.command_name, self.datetime_format):
            match self.command_opts:
                case ['--format=']:
                    return self.repository.get_current_datetime(timezone, self.datetime_format)
                case ['--format=', '-s']:
                    return self.repository.set_datetime_format(self.datetime_format)
        if '--Set=' or '-s' in self.command_opts:
            if self.validator.validate_date_format(self.command_name, self.datetime_format):
                match self.command_opts:
                    case ['--Set=']:
                        return self.repository.set_datetime_format(self.datetime_format)
                    case ['-s']:
                        return self.repository.set_datetime_format(self.datetime_format)

        return InvalidCommandFormatError(self.command_name, self.command_format)

    def sleep_command(self):
        return self.command_name, self.command_args

    @staticmethod
    @pysnooper.snoop()
    def uptime_command(additional_parameters):
        current_time = additional_parameters[2]
        return current_time

    @staticmethod
    @pysnooper.snoop()
    def set_variable_splitter(self, variable, datestr, lst):
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

    def additional_requirements(self, tokens):
        match self.command_name:
            case 'date':
                self.remove_none_values()
                self.sort_datetime_format(tokens)
                return True
        return False

    def sort_datetime_format(self, tokens):
        for token in tokens:
            if token.startswith('--format='):
                self.datetime_format, tokens = self.set_variable_splitter('--format=', token, tokens)
            if token.startswith('--Set='):
                self.datetime_format, tokens = self.set_variable_splitter('--Set=', token, tokens)

    def build(self, tokens):
        self.command_args = self.determine_command_arguments(self.command_name, self.command_format[1], tokens[1:])
        self.command_opts = self.determine_command_options(self.command_name, self.command_format[2], tokens[1:])
        self.command = [self.command_name, self.command_args, self.command_opts]

    def parse(self, tokens):
        self.command_format = self.establish_command_format(tokens[0])
        self.command_name = self.command_format[0]
        self.validator.validate_command(tokens, self.command_name, self.command_format)
        self.build(tokens)
        return self.additional_requirements(tokens)

    def execute_command(self, additional_parameters=None):
        match self.command_name:
            case 'help':
                return self.help_command()
            case 'clear':
                return self.clear_command()
            case 'history':
                return self.history_command()
            case 'date':
                self.remove_none_values()
                return self.date_command(additional_parameters)
            case 'sleep':
                return self.sleep_command()
            case 'uptime':
                return self.uptime_command(additional_parameters)

    def run_command(self, command_statement, additional_details):
        if self.parse(command_statement.split(' ')):
            additional_details = self.additional_details
        return self.execute_command(additional_details)



