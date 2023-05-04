from src.Models.Commands.commands import Command


class Ls(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_ls_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_ls_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Cp(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_cp_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_cp_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Rm(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_rm_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_rm_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Mv(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_mv_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_mv_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Chmod(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_chmod_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_chmod_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Chown(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_chown_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_chown_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()

