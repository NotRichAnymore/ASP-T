import re

class Command:
    def __init__(self, cmd_name, args):
        self.command_name = cmd_name
        self.arguments = args

    def set_command_name(self, cmd_name):
        self.command_name = cmd_name

    def parse_command(self):
        try:
            for cmd in self.validCommands:
                if cmd == self.command_name:
                    self.set_command_name(cmd)
                    return f'execute_{cmd}_command'
                else:
                    raise IOError
        except IOError as ioe:
            create_error_message(type='parse', message='Valid command not found', error_response=str(ioe))

    def parse_argument(self):
        try:
            # Get command arguments dict from file
            valid_command_arguments = self.valid_command_arguments()
            # Get the command name from the dict keys
            command_name_from_dict = valid_command_arguments.keys()

            # check that the user selected command is found in the dict
            for command_name in command_name_from_dict:
                if self.command_name == command_name:
                    # if so get the corresponding list of arguments for the command
                    file_args = valid_command_arguments[self.command_name()]

                    chosen_arguments = {'':''}
                    # for each chosen argument get the matching file argument
                    for chosen_arg, file_arg in zip(self.arguments, file_args):
                        # Use regex to check if the argument is valid
                        regex = r"(^\A-+)([a-z]$)"
                        matches = re.Match(regex, chosen_arg, re.MULTILINE)
                        if matches:
                            # Check if the argument is not avaiable for this command or just has a few arguments
                            # aka less arguments that the max allowed
                            if chosen_arg == file_arg:
                                chosen_arguments.update('Valid Argument', file_arg)
                            elif chosen_arg != file_arg:
                                chosen_arguments.update('Invalid Argument', file_arg)
                            elif chosen_arg is None:
                                chosen_arguments.update('No Argument')

                    # if the number of chosen arguments exceeds the number of arguments
                    # from the list then index error raised
                    if len(chosen_arguments) > len(file_args):
                        raise IndexError



                raise IOError
        except (IOError, IndexError) as (ioe, ine):
            create_error_message(type='parse', message='Valid command not found', error_response=str(ioe))
