from src.components.Utilities.utilities import create_error_message


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

    def parse_command(self, user_defined_command):
        command_name = self.repository.get_command_name
        command_type = self.repository.get_command_type(user_defined_command)
        print('Validating command')
        if self.validator.validate_command(command_name, user_defined_command):
            print('Command valid')
            return user_defined_command, command_type

    def parse_command_arguments(self, user_defined_arguments):
        command_arguments = self.repository.get_command_arguments(user_defined_arguments)

        if self.validator.validate_command_arguments(command_arguments, user_defined_arguments):
            return command_arguments

    def parse_command_options(self, user_defined_options):
        command_options = self.repository.get_command_options(user_defined_options)

        if self.validator.validate_command_options(command_options, user_defined_options):
            return command_options

    def determine_argument_order(self, user_input):
        split_string = user_input.split(' ')
        self.command_name = split_string[0]
        arguments = self.repository.get_arguments_from_command_name(self.command_name)
        options = self.repository.get_options_from_command_name(self.command_name)
        for arg, opt, string_element in zip(arguments, options, split_string):
            if not split_string[string_element] == 0:
                match string_element:
                    case str(arg) if str(arg) != 'None':
                        self.add_command_argument(string_element)
                    case str(opt) if str(opt) != 'None':
                        self.add_command_option(string_element)

        return self.command_name, self.command_arguments, self.command_options

    def parse(self, user_input):
        user_defined_command, user_defined_arguments, user_defined_options = \
            self.determine_argument_order(user_input)

        command_name, command_type = self.parse_command(user_defined_command)
        command_arguments = self.parse_command_arguments(user_defined_arguments)
        command_options = self.parse_command_options(user_defined_options)

        status, valid_parses, invalid_parses = self.validator.parse_successful()
        if status and invalid_parses is None:
            self.validator.reset()
            return self.repository.create_command_object(command_name, command_arguments, command_options, command_type)
        else:
            return create_error_message(error_type='parse',
                                        message='Unable to parse user input',
                                        error_message=None)

    def run_command(self, command):
        pass
