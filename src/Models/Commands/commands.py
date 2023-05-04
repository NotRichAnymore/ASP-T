class Command:
    def __init__(self, cmd_name, args=None, opts=None):
        self.command_name = cmd_name
        self.arguments = args
        self.options = opts

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



    