from src.Models.Commands.commands import Command


class Date(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_date_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_date_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Sleep(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_sleep_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_sleep_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Uptime(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_uptime_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_uptime_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()
