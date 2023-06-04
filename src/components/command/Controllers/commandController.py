


class CommandController:

    def __init__(self, service):
        self.service = service

    def execute_command(self, command_arguments, additional_parameters):
        try:
            command_name = self.service.parse(command_arguments)
            if command_name:
                match command_name:
                    case 'date':
                        return self.service.run_command(additional_parameters)
            return self.service.run_command()
        except Exception as e:
            return e








