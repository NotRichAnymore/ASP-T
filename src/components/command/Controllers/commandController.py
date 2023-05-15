


class CommandController:

    def __init__(self, service):
        self.service = service

    def load_command(self, command_arguments):
        return self.service.parse(command_arguments)

    def run_command(self, command):
        return self.service.run_command(command)








