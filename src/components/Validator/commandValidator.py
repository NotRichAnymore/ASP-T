from src.components.Utilities.utilities import create_error_message

import re


class CommandValidator:
    def __init__(self):
        self.valid_command = None
        self.valid_arguments = None
        self.valid_options = None
        self.valid_parses = []
        self.invalid_parses = []

    def add_valid_parse(self, parse_type):
        self.valid_parses.append(parse_type)

    def add_invalid_parse(self, parse_type):
        self.invalid_parses.append(parse_type)

    def validate_command(self, user_defined_command, commands_from_repo):
        try:
            parse_type = 'command'
            for cmd in commands_from_repo:
                if cmd == user_defined_command:
                    self.add_valid_parse(parse_type)
                    self.valid_command = True
                else:
                    self.add_invalid_parse(parse_type)
                    self.valid_command = False
                    raise IOError
        except IOError as ioe:
            return create_error_message(error_type='validate',
                                        message=f'Unable to validate command: {user_defined_command}',
                                        error_message=str(ioe))

    def validate_command_arguments(self, user_defined_arguments, arguments_from_repo):
        parse_type = 'arguments'
        valid_user_args = []
        try:
            for user_args, file_args in zip(user_defined_arguments, arguments_from_repo):
                # Check that the arguments is present in the database
                # Compare the user defined args against the ones from the database
                match user_args:
                    case user_args if user_args == file_args:
                        valid_user_args.append(user_args)
                    case user_args if user_args != file_args:
                        self.add_invalid_parse(parse_type)
                        self.valid_arguments = False
                        raise IOError

            if len(valid_user_args) == len(user_defined_arguments):
                self.add_valid_parse(parse_type)
                self.valid_arguments = True
            else:
                raise IOError
        except IOError as ioe:
            return create_error_message(error_type='validate',
                                        message=f'Unable to validate arguments: '
                                                f'{",".join(arg for arg in user_defined_arguments)}',
                                        error_message=str(ioe))

    def validate_command_options(self, user_defined_options, options_from_repo):
        try:
            # Get command options from database
            # check that the user selected options is found in the database
            parse_type = 'options'
            valid_user_options = []
            # for each chosen option get the matching db option
            for user_opt, file_opt in zip(user_defined_options, options_from_repo):
                # Use regex to check if the option is valid
                regex = r"(^\A-+)([a-z]$)"
                matches = re.Match(regex, user_opt, re.MULTILINE)
                if matches:
                    # Check if the option is not available for this command or just has a few options
                    # aka fewer options that the max allowed
                    # ^ need consideration before implementing
                    match user_opt:
                        case user_opt if user_opt == file_opt:
                            valid_user_options.append(user_opt)
                        case user_opt if user_opt != file_opt:
                            self.add_invalid_parse(parse_type)
                            self.valid_arguments = False
                            raise IOError
                
                    # if the number of chosen options exceeds the number of options
                    # from the list then index error raised
                if len(valid_user_options) == len(options_from_repo):
                    self.add_valid_parse(parse_type)
                    self.valid_options = True

        except IOError as e:
            return create_error_message(error_type='validate',
                                        message=f'Unable to validate options: '
                                                f'{",".join(opt for opt in user_defined_options)}',
                                        error_message=str(e))

    def parse_successful(self):
        if self.valid_command and self.valid_arguments and self.valid_options:
            return True, self.valid_parses, None
        return False, self.valid_parses, self.invalid_parses

    def reset(self):
        self.valid_command, self.valid_arguments, self.valid_options = None, None, None
        self.valid_parses, self.invalid_parses = [], []
        
