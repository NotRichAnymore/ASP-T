


class CommandController:

    def __init__(self, service):
        self.service = service

    def execute_command(self, command_arguments, additional_parameters):
        try:
            return self.service.run_command(command_arguments, additional_parameters)
        except Exception as e:
            return e

    def save_command_response(self, command_response, save_folder, write=None, read=None, startup=None):
        if write:
            self.service.write_command_response(command_response=command_response, save_folder=save_folder)
        if read:
            return self.service.read_command_history(save_folder=save_folder)
        if startup:
            self.service.write_command_response(command_response=command_response, save_folder=save_folder, clear_file=True)







