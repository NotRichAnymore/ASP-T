


class CommandController:

    def __init__(self, service):
        self.service = service

    def execute_command(self, command_arguments, additional_parameters):
        try:
            return self.service.run_command(command_arguments, additional_parameters)
        except Exception as e:
            return e








