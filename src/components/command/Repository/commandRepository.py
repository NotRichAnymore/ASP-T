import json
import pysnooper
from pathlib import Path
from src.components.command.Models.Commands.commands import Command
from src.components.Utilities.sqliteUtilities import SqliteUtilities


@pysnooper.snoop()
class CommandRepository:

    def __init__(self):
        self.command = Command(None)
        self.initial_sql = SqliteUtilities()
        self.database_path = None
        self.command_details_path = Path('src').resolve().parent.parent\
            .joinpath('data/files/command_details.json').as_posix()
        self.datetime_formats_path = Path('src').resolve().parent.parent\
            .joinpath('data/files/datetime_formats.json').as_posix()
        self.help_command_details_path = Path('src').resolve().parent.parent\
            .joinpath('data/files/help_command_details.json')

    def create_command_object(self, command_name, command_arguments, command_options, command_type):
        return self.command.create_command_object(command_name, command_arguments, command_options, command_type)

    def read_command_details(self):
        with open(self.command_details_path, "r") as file:
            jsonObj = json.load(file)
            return jsonObj

    def get_all_commands(self):
        commands = []
        jsonObject = self.read_command_details()
        for index in range(len(jsonObject)):
            commands.append(jsonObject[index]['name'])
        return commands

    def get_command_format(self, command):
        jsonObject = self.read_command_details()
        for index in range(len(jsonObject)):
            if jsonObject[index]['name'] == command:
                return jsonObject[index]['name'], jsonObject[index]['arguments'], jsonObject[index]['options']


    def read_datetime_formats(self):
        with open(self.datetime_formats_path, "r") as file:
            jsonObj = json.load(file)
            return jsonObj

    def get_all_datetime_formats(self):
        datetime_formats = []
        jsonObject = self.read_datetime_formats()
        for index in range(len(jsonObject)):
            datetime_formats.append(jsonObject[index]['Date'])
        return datetime_formats

    def read_help_command_details(self):
        with open(self.help_command_details_path, 'r') as file:
            jsonObj = json.load(file)
            return jsonObj

    def get_all_help_command_details(self):
        return self.read_help_command_details()

