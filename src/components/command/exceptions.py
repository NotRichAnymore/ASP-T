


class InvalidCommandFormatError(Exception):
    """
    Exception raised for errors in a command's format
    Attributes:
    command -- The name of the instruction defined by the user
    format -- The order in which the command should be written
    message -- Explanation of the occurring error
    """
    def __init__(self, command, command_format):
        self.command = command
        self.format = command_format
        self.message = f"{command} command fails to follow it's format: {command_format}"
        super().__init__(self.message)
