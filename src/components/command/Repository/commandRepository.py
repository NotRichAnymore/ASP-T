import ctypes
import datetime
import json
import os
import time
import re
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
        self.command_details_path = Path('src').resolve().parent.parent \
            .joinpath('data/files/command_details.json').as_posix()
        self.datetime_formats_path = Path('src').resolve().parent.parent \
            .joinpath('data/files/datetime_formats.json').as_posix()
        self.help_command_details_path = Path('src').resolve().parent.parent \
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

    def get_directory_and_filenames(self, path):
        directories = []
        files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            files.extend(filenames)
            directories.extend(dirnames)
            break
        return directories, files

    def has_hidden_attribute(self, filepath):
        return bool(os.stat(filepath).st_file_attributes)

    def sort_mod_time(self, mod_time):
        return sorted(mod_time, reverse=True)

    def convert_mod_time_to_date(self, sorted_mod_time):
        return [time.ctime(mod_time) for mod_time in sorted_mod_time]

    def get_directory_details(self, path, dirnames):
        details = []
        for directory in dirnames:
            dirpath = path + '/' + directory
            try:
                stat_result = os.stat_result(os.stat(dirpath))
            except FileNotFoundError:
                continue

            owner = stat_result.st_uid
            group = stat_result.st_gid
            permissions = stat_result.st_mode
            last_access = stat_result.st_atime
            last_modification = stat_result.st_mtime
            file_created = stat_result.st_ctime
            # file_type = stat_result.st_type
            file_size = stat_result.st_size / 1024

            directory_details = f'{directory} ' \
                                f'\nOwner: {owner}' \
                                f'\nGroups: {group}' \
                                f'\nPermissions: {permissions}' \
                                f'\nLast Access: {last_access}' \
                                f'\nLast Modification: {last_modification}' \
                                f'\nFile Created At: {file_created}' \
                                f'\nFile Size: {file_size} MB\n'
            details.append(directory_details)

        return details

    def get_hidden_files(self, path, filenames):
        hidden_files = []
        for file in filenames:
            filepath = path + '/' + file
            if filepath.startswith('.') or self.has_hidden_attribute(filepath):
                hidden_files.append(file)
        return hidden_files

    def get_modification_dates(self, path, filenames):
        mod_time = []
        for file in filenames:
            filepath = path + '/' + file
            mod_time.append(os.path.getmtime(filepath))
        sorted_mod_time = self.sort_mod_time(mod_time)
        sorted_mod_date = self.convert_mod_time_to_date(sorted_mod_time)
        return [f'{file} {mod_date}' for file, mod_date in zip(filenames, sorted_mod_date)]

    def get_reversed_directory_contents(self, filenames, dirnames):
        reversed_files = [file for file in reversed(filenames)]
        reversed_directories = [directory for directory in reversed(dirnames)]
        return reversed_files, reversed_directories

    def get_directory_contents(self, path, show_hidden=None, only_directory=None, directory_details=None,
                               modification_date=None, in_reverse=None):

        dirnames, filenames = self.get_directory_and_filenames(path)
        [filenames.remove(file) for file in filenames if re.match(r"^(\.[a-zA-z])|^(\.[0-9])", file)]
        directory_contents = [
            {
                "type": "directory",
                "data": dirnames,
                "colour": "Blue"
            },
            {
                "type": "files",
                "data": filenames,
                "colour": "Green"
            },
            {
                "type": "hidden_files",
                "data": [''],
                "colour": "Purple"
            }

        ]

        if only_directory:
            directory_contents[1]['data'] = ['']

        if directory_details:
            directory_contents[0]['data'] = self.get_directory_details(path, dirnames)
            directory_contents[1]['data'] = self.get_directory_details(path, filenames)

        if show_hidden:
            directory_contents[2]['data'] = self.get_hidden_files(path, filenames)

        if modification_date:
            directory_contents[1]['data'] = self.get_modification_dates(path, filenames)

        if in_reverse:
            reversed_files, reversed_directories = self.get_reversed_directory_contents(filenames, dirnames)
            directory_contents[0]['data'] = reversed_files
            directory_contents[1]['data'] = reversed_directories

        return directory_contents


