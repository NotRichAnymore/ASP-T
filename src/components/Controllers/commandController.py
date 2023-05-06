from src.components.Models.Commands import commands
from datetime import date
import time


class CommandController:

    def __init__(self, service):
        self.service = service
        self.command = commands.Command(None)

    def load_command(self, command_arguments):
        return self.service.parse(command_arguments)

    def run_command(self, command):
        return self.service.run_command(command)








