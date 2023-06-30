import ctypes
import datetime
import json
import os
import time
import re
import pysnooper
import pytz
import shutil
import tempfile
import filecmp
import fileinput
from pathlib import Path
from src.components.command.Models.Commands.commands import Command
from src.components.Utilities.sqliteUtilities import SqliteUtilities
from src.components.Utilities.mySQLUtilities import MySQLUtilities


@pysnooper.snoop()
class CommandRepository:

    def __init__(self):
        self.backup_dir = None
        self.dest_path = None
        self.src_path = None
        self.backup_file = None
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
            last_access = datetime.datetime.fromtimestamp(stat_result.st_atime).strftime('%Y-%m-%d %H:%M')
            last_modification = datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime('%Y-%m-%d %H:%M')
            file_created = datetime.datetime.fromtimestamp(stat_result.st_ctime).strftime('%Y-%m-%d %H:%M')
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

    def write_json_object_to_file(self, save_path, file_mode, obj):
        with open(save_path, file_mode) as json_file:
            json.dump(obj, json_file)

    def read_json_object_from_file(self, save_path):
        with open(save_path, 'r') as json_file:
            return json.load(json_file)

    def append_json_object_to_file(self, save_path, command_response):
        jsonObj = self.read_json_object_from_file(save_path)
        jsonObj.append(command_response[0])
        with open(save_path, 'w') as json_file:
            json.dump(jsonObj, json_file)

    def clear_file(self, save_path):
        with open(save_path, 'w') as json_file:
            pass

    def successful_backup(self, path=None, backup_file=None):
        return filecmp.cmp((self.src_path if path is None else path),
                           (self.backup_file.name if backup_file is None else backup_file))

    def get_filepaths_from_directory(self):
        paths = []
        for (dirpath, dirnames, filenames) in os.walk(self.src_path):
            for file in filenames:
                paths.append(Path(dirpath).joinpath(file))
        return paths

    def create_backup(self):
        _suffix = str(Path('_' + Path(self.src_path).stem + '_backup' + Path(self.src_path).suffix))
        self.backup_file = tempfile.NamedTemporaryFile(mode='w+',
                                                       newline='\n',
                                                       suffix=_suffix,
                                                       dir=Path(self.src_path).parent)

        if Path(self.src_path).is_file():
            _suffix = str(Path('_' + Path(self.src_path).stem + '_backup' + Path(self.src_path).suffix))
            self.backup_file = tempfile.NamedTemporaryFile(mode='w+',
                                                           newline='\n',
                                                           suffix=_suffix,
                                                           dir=Path(self.src_path).parent)
            with open(self.src_path, 'r') as src_file:
                for line in src_file:
                    self.backup_file.write(line)

            if Path(self.backup_file.name).exists():
                return self.successful_backup()
            return False

        elif Path(self.src_path).is_dir():
            backup_created = []
            paths = self.get_filepaths_from_directory()
            self.backup_dir = tempfile.TemporaryDirectory(dir=self.src_path)
            for path in paths:
                _suffix = str(Path('_' + Path(path).stem + '_backup' + Path(path).suffix))
                backup_file = tempfile.NamedTemporaryFile(mode='w+',
                                                          newline='\n',
                                                          suffix=_suffix,
                                                          dir=self.backup_dir.name)
                with open(path, 'r') as src_file:
                    for line in src_file:
                        backup_file.write(line)

                if Path(backup_file.name).exists():
                    backup_created.append(True if self.successful_backup(path, self.backup_file.name) else False)

            if len(paths) == len(backup_created) and False not in backup_created:
                return True

        return False

    def close_backup(self):
        if self.backup_file and Path(self.backup_files.name).exists():
            self.backup_file.close()

        if self.backup_dir and Path(self.backup_dir.name).exists():
            self.backup_dir.cleanup()



    def copy_path(self, src_path, dest_path,
                  file_to_file=None, file_to_directory=None, directory_to_directory=None,
                  backup=None, debug=None, force=None, no_clobber=None, recursive=None,
                  remove_dest=None, suffix=None, target_directory=None, no_target_directory=None, verbose=None):

        self.src_path = src_path
        self.dest_path = dest_path
        success = False

        # variable: check file type
        # variable: check if dest path is empty or has contents
        # variable(s): check which options are True

        same_file_type = True
        src_file_type, dest_file_type = self.get_file_types(src_path, dest_path)
        if Path(src_path).suffix != Path(dest_path).suffix:
            same_file_type = False

        has_contents = self.dest_has_contents(dest_path)

        # Prepatory Options
        if backup:
            # create temp file of src
            # delete before exit
            if not self.create_backup():
                return success

        if no_target_directory and dest_path is None:
            dest_path = src_path

        # Main Functionality
        if file_to_file:
            # conditional: if empty read from src and write in dest
            # conditional: if has contents depending on file type append to existing contents
            # variable: check if contents from src are in contents from dest then return
            pass

        if file_to_directory:
            pass

        if directory_to_directory:
            pass

        self.close_backup()
        return success
