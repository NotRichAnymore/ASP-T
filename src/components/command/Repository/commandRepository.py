import datetime
import json
import pysnooper
import pytz
from pathlib import Path
from src.components.command.Models.Commands.commands import Command
from src.components.Utilities.sqliteUtilities import SqliteUtilities
from src.components.Utilities.mySQLUtilities import MySQLUtilities


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

    def get_all_command_details(self):
        return self.read_command_details()

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
            datetime_formats.append(jsonObject[index]['Data'])
        return datetime_formats

    def get_current_time(self):
        return datetime.datetime.now().time()

    def get_current_date(self):
        return datetime.datetime.now().date()

    def get_current_datetime(self, timezone, fmt=None):
        if isinstance(timezone, str):
            timezone = pytz.timezone(timezone)
        if fmt:
            return datetime.datetime.now().astimezone(timezone).strftime(fmt)
        return datetime.datetime.now().astimezone(timezone)

    def set_datetime_format(self, fmt):
        return 'date', fmt

    @staticmethod
    def get_global_datetimes(fmt=None):
        global_datetimes = []
        for timezone in pytz.common_timezones:
            dt = datetime.datetime.now().astimezone(pytz.timezone(timezone))
            if fmt:
                dt = dt.strftime(fmt)
            global_datetimes.append(f'[{pytz.timezone(timezone).zone}]|[{dt}]')
        return global_datetimes

    def read_help_command_details(self):
        with open(self.help_command_details_path, 'r') as file:
            jsonObj = json.load(file)
            return jsonObj

    def get_all_help_command_details(self):
        return self.read_help_command_details()

