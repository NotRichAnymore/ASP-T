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

        if self.validator.validate_command(command_name, user_defined_command):
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

        if self.validator.parse_successful():
            self.validator.reset()
            return self.repository.create_command_object(command_name,command_arguments, command_options, command_type)

    def run_command(self, command):
        pass
#     def parse_command(self, user_defined_command):
#         
#
#
#     def parse_arguments(self, user_defined_arguments):
#         command_name = self.command.get_command_name()
#         valid_command_arguments = self.get_valid_arguments()
#         valid_user_args = None
#         try:
#             for command_name_file in valid_command_arguments.keys():
#                 # Check that the command is present in the file
#                 if command_name == command_name_file:
#                     file_arguments = valid_command_arguments[command_name]
#                     # Compare the user defined args against the ones from the file
#                     for user_args, file_args in zip(user_defined_arguments, file_arguments):
#                         for cmd_name in self.get_valid_commands():
#                             match cmd_name:
#                                 case 'help':
#                                     if user_args in self.get_valid_commands():
#                                         valid_user_args = True
#                                 case ['clear', 'history', 'uptime', 'pwd', 'shutdown', 'halt', 'reboot', 'top']:
#                                     if user_args is None:
#                                         valid_user_args = True
#                                 case 'date':
#                                     if self.valid_date_format(user_args):
#                                         valid_user_args = True
#                                 case 'sleep':
#                                     if self.valid_sleep_format(user_args):
#                                         valid_user_args = True
#                                 case ['id', 'groups', 'passwd', 'last']:
#                                     if user_args in self.get_user_list():
#                                         valid_user_args = True
#                                 case 'who':
#                                     if user_args == 'am i':
#                                         valid_user_args = True
#                                 case 'ls':
#                                     if Path(user_args).is_dir():
#                                         valid_user_args = True
#                                 case 'cp':
#                                     if Path(user_args[0]).exists() and Path(user_args[1]).exists():
#                                         valid_user_args = True
#                                 case ['rm', 'cat', 'more', 'head', 'less', 'tail']:
#                                     if Path(user_args).is_file():
#                                         valid_user_args = True
#                                 case 'mv':
#                                     if (Path(user_args[0]).is_file() and Path(user_args[1]).is_file()) or\
#                                             (Path(user_args[0]).is_file() and Path(user_args[1]).is_dir()):
#                                         valid_user_args = True
#                                 case ['chown', 'chmod']:
#                                     if user_args[0] in self.get_permissions_list and \
#                                             (Path(user_args[1]).is_file() or Path(user_args[1]).is_file()):
#                                         valid_user_args = True
#                                 case 'grep':
#                                     if isinstance(user_args[0], str) and Path(user_args[1]).is_file():
#                                         valid_user_args = True
#                                 case 'ln':
#                                     if Path(user_args[0]).is_absolute() and isinstance(user_args[1], str):
#                                         valid_user_args = True
#                                 case ['mkdir', 'rmdir']:
#                                     if Path(user_args).is_dir():
#                                         valid_user_args = True
#                                 case 'ps':
#                                     if isinstance(user_args, int):
#                                         valid_user_args = True
#                                 case 'kill':
#                                     if isinstance(user_args[0], int) and isinstance(user_args[1], int):
#                                         valid_user_args = True
#                     if valid_user_args:
#                         return file_arguments
#                     else:
#                         raise IOError
#         except IOError as ioe:
#             return create_error_message(error_type='parse', message=f'Unable to get arguments for {command_name}',
#                                         error_message=str(ioe))
#
#
#
#     def parse_option(self, user_defined_options):
#         try:
#             # Get command options dict from file
#             command_name = self.command.get_command_name()
#             valid_command_options = self.get_valid_options()
#             # Get the command name from the dict keys and
#             # check that the user selected command is found in the dict
#             for command_name_file in valid_command_options.keys():
#                 if command_name == command_name_file:
#                     # if so get the corresponding list of options for the command
#                     file_options = valid_command_options[command_name]
#
#                     chosen_options = {'': ''}
#                     # for each chosen option get the matching file option
#                     for chosen_opt, file_opt in zip(user_defined_options, file_options):
#                         # Use regex to check if the option is valid
#                         regex = r"(^\A-+)([a-z]$)"
#                         matches = re.Match(regex, chosen_opt, re.MULTILINE)
#                         if matches:
#                             # Check if the option is not available for this command or just has a few options
#                             # aka fewer options that the max allowed
#                             if chosen_opt == file_opt:
#                                 chosen_options.update({'Valid option', file_opt})
#                             elif chosen_opt != file_opt:
#                                 chosen_options.update({'Invalid option', file_opt})
#                             elif chosen_opt is None:
#                                 chosen_options.update('No option')
#
#
#                     # if the number of chosen options exceeds the number of options
#                     # from the list then index error raised
#                     if len(chosen_options) > len(file_options):
#                         raise IndexError
#
#                     no_option = 0
#                     valid_option = 0
#                     for chosen_opt in chosen_options:
#                         match chosen_opt:
#                             case 'Invalid option':
#                                 raise IOError
#                             # If chosen_options contains no options or is none then raise IOError
#                             case 'No option':
#                                 no_option += 1
#                                 if no_option < 1:
#                                     raise IOError
#                             # If all chosen_options return dict
#                             case 'Valid option':
#                                 valid_option += 1
#                                 if valid_option == len(chosen_options):
#                                     return chosen_options
#
#         except (IOError, IndexError) as e:
#             return create_error_message(error_type='parse', message=f'Options {user_defined_options} are not valid',
#                                         error_message=str(e))
