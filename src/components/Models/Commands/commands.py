class Command:
    def __init__(self, cmd_name, args=None, opts=None):
        self.command_name = cmd_name
        self.arguments = args
        self.options = opts
        self.cmd_type = None

    def set_command_name(self, cmd_name):
        self.command_name = cmd_name

    def get_command_name(self):
        return self.command_name

    def set_command_arguments(self, args):
        self.arguments = args

    def get_command_arguments(self):
        return self.arguments

    def set_command_options(self, opt):
        self.options = opt

    def get_command_options(self):
        return self.options

    def set_command_type(self, typ):
        self.cmd_type = typ

    def get_command_type(self):
        return self.cmd_type

    def create_command_object(self, command_name, command_arguments, command_options, command_type):
        self.set_command_name(command_name)
        self.set_command_arguments(command_arguments)
        self.set_command_options(command_options)
        self.set_command_type(command_type)

        return self
