import re
from src.Models.Commands import commands
from src.Utilities.utilities import create_error_message


class CommandController:

    def __init__(self):
        self.command = commands.Command(None, None)

    def parse_command(self, user_defined_command):
        commands_from_file = self.command.get_valid_commands()
        try:
            for cmd in commands_from_file:
                if cmd == user_defined_command:
                    self.command.set_command_name(cmd)
                    return f'execute_{cmd}_command'
                else:
                    raise IOError
        except IOError as ioe:
            return create_error_message(error_type='parse', message='Valid command not found', error_message=str(ioe))

    def parse_argument(self, user_defined_arguments):
        try:
            # Get command arguments dict from file
            command_name = self.command.get_command_name()
            valid_command_arguments = self.command.get_valid_arguments(command_name)
            # Get the command name from the dict keys and
            # check that the user selected command is found in the dict
            for command_name_file in valid_command_arguments.keys():
                if command_name == command_name_file:
                    # if so get the corresponding list of arguments for the command
                    file_arguments = valid_command_arguments[command_name]

                    chosen_arguments = {'': ''}
                    # for each chosen argument get the matching file argument
                    for chosen_arg, file_arg in zip(user_defined_arguments, file_arguments):
                        # Use regex to check if the argument is valid
                        regex = r"(^\A-+)([a-z]$)"
                        matches = re.Match(regex, chosen_arg, re.MULTILINE)
                        if matches:
                            # Check if the argument is not available for this command or just has a few arguments
                            # aka fewer arguments that the max allowed
                            if chosen_arg == file_arg:
                                chosen_arguments.update({'Valid Argument', file_arg})
                            elif chosen_arg != file_arg:
                                chosen_arguments.update({'Invalid Argument', file_arg})
                            elif chosen_arg is None:
                                chosen_arguments.update('No Argument')


                    # if the number of chosen arguments exceeds the number of arguments
                    # from the list then index error raised
                    if len(chosen_arguments) > len(file_arguments):
                        raise IndexError

                    for chosen_arg in chosen_arguments:
                        match chosen_arg:
                            case 'Invalid Argument':
                                raise IOError
                            # If chosen_arguments contains no arguments or is none then raise IOError
                            case 'No Argument':
                                raise IOError
                            # If chosen_arguments contains at least one valid argument return dict
                            case 'Valid Argument':
                                return chosen_arguments

        except (IOError, IndexError) as (ioe, ine):
            return create_error_message(error_type='parse', message='Valid command not found', error_message=str(ioe))
