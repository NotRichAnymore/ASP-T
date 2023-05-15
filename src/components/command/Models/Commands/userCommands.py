from src.components.command.Models.Commands.commands import Command


class Whoami(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_whoami_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_whoami_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Id(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_id_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_id_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Groups(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_groups_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_groups_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Passwd(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_passwd_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_passwd_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Who(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_who_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_who_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Last(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_passwd_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_passwd_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()
