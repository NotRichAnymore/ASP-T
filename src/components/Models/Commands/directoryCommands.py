from src.components.Models.Commands.commands import Command


class Cd(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_cd_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_cd_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Pwd(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_pwd_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_pwd_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Ln(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_ln_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_ln_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Mkdir(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_mkdir_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_mkdir_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Rmdir(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_rmdir_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_rmdir_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()