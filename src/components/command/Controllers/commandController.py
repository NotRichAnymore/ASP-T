


class CommandController:

    def __init__(self, service):
        self.service = service

    def load_command(self, command_arguments):
        self.service.parse(command_arguments)

    def run_command(self):
        return self.service.run_command()








