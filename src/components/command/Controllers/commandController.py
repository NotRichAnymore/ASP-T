


class CommandController:

    def __init__(self, service):
        self.service = service

    def execute_command(self, command_arguments):
        try:
            self.service.parse(command_arguments)
            return self.service.run_command()
        except Exception as e:
            return e








