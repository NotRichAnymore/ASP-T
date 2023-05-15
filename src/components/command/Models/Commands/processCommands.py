from src.components.command.Models.Commands.commands import Command


class Ps(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_ps_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_ps_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Top(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_top_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_top_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Kill(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_kill_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_kill_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()
