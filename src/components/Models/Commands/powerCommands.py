from src.components.Models.Commands.commands import Command


class Shutdown(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_shutdown_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_shutdown_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Halt(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_halt_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_halt_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Reboot(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_reboot_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_reboot_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()
