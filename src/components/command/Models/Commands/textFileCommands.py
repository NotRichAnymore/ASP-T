from src.components.command.Models.Commands.commands import Command


class Cat(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_cat_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_cat_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class More(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_more_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_more_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Less(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_less_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_less_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Head(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_head_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_head_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Tail(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_tail_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_tail_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()


class Grep(Command):
    def __init__(self, command_name, arguments, options):
        super().__init__(command_name, arguments, options)

    def initialise_grep_command(self):
        self.set_command_name(self.command_name)
        self.set_command_arguments(self.arguments)
        self.set_command_options(self.options)

    def get_grep_command(self):
        return self.get_command_name(), self.get_command_arguments(), self.get_command_options()

