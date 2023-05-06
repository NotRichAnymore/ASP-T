from src.components.Models.Commands.commands import Command


class Help(Command):
    def __init__(self, command_name, arguments, options, typ):
        super().__init__(command_name, arguments, options)
        self.cmd_type = typ

    def initialise_help_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)
        self.set_command_type(self.cmd_type)

    def get_help_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Clear(Command):
    def __init__(self, command_name, arguments, options, typ):
        super().__init__(command_name, arguments, options)
        self.cmd_type = typ

    def initialise_clear_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)
        self.set_command_type(self.cmd_type)

    def get_clear_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class History(Command):
    def __init__(self, command_name, arguments, options, typ):
        super().__init__(command_name, arguments, options)
        self.cmd_type = typ

    def initialise_history_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)
        self.set_command_type(self.cmd_type)

    def get_history_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()

