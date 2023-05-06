from src.components.Models.Commands import commands
from datetime import date
import time


class CommandController:

    def __init__(self, service):
        self.service = service
        self.command = commands.Command(None)

        

    def valid_date_format(self, date_format):
        try:
            date.strftime(date.today(), date_format)
            return True
        except Exception as e:
            print(e)
            return False


    def valid_sleep_format(self, time_format):
        try:
            time.strftime(time.localtime(), time_format)
            return True
        except Exception as e:
            print(e)
            return False


    def load_command(self, command_arguments):
        return self.service.parse(command_arguments)

    def run_command(self, command):
        return self.service.run_command(command)








