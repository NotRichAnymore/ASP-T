from src.components.Models.Commands.commands import Command
from src.components.Utilities.sqliteUtilities import SqliteUtilities

class CommandRepository:

    def __init__(self):
        self.command = Command(None)
        self.initial_sql = SqliteUtilities()
        self.database_path = None

    def create_command_object(self, command_name, command_arguments, command_options, command_type):
        return self.command.create_command_object(command_name, command_arguments, command_options, command_type)

    def create_initial_tables(self):
        table_list = self.command_table(), self.argument_table(), self.options_table()
        self.initial_sql.create_initial_tables(self.database_path, table_list)

    def get_by_path(self, path):
        pass

    def get_command_arguments(self):
        pass

    def get_command_options(self):
        pass

    def get_command_type(self):
        pass

    def get_arguments_from_command_name(self, command_name):
        pass

    def get_options_from_command_name(self, command_name):
        pass

    def command_table(self):
        pass

    def argument_table(self):
        pass

    def options_table(self):
        pass

#  def valid_date_format(self, date_format):
#         try:
#             date.strftime(date.today(), date_format)
#             return True
#         except Exception as e:
#             print(e)
#             return False
#
#
#     def valid_sleep_format(self, time_format):
#         try:
#             time.strftime(time.localtime(), time_format)
#             return True
#         except Exception as e:
#             print(e)
#             return False
# self.command_list_path = Path('src').resolve().parent\
#             .joinpath('data/files/command_list.json').as_posix()
#
#         self.arguments_list_path = Path('src').resolve().parent\
#             .joinpath('data/files/command_arguments_list.json').as_posix()
#
#         self.options_list_path = Path('src').resolve()\
#             .parent.joinpath('data/files/command_options_list.json').as_posix()
#
#         self.user_list_path = Path('src').resolve()\
#             .parent.joinpath('data/files/users.json').as_posix()
#
#         self.permissions_list_path = Path('src').resolve()\
#             .parent.joinpath('data/files/permissions.json').as_posix()
#
#     def get_command_paths(self):
#         return [self.command_list_path, self.arguments_list_path, self.options_list_path]
#
#
#     def get_valid_commands(self):
#         try:
#             command_list = {}
#             with open(self.command_list_path) as file:
#                 command_list.update(json.load(file))
#             return command_list
#         except FileNotFoundError as fNfE:
#             return create_error_message(error_type='file', message='Unable to obtain valid commands',
#                                         error_message=str(fNfE))
#
#
#     def get_valid_arguments(self):
#         try:
#             arguments_list = {}
#             with open(self.arguments_list_path) as file:
#                 arguments_list.update(json.load(file))
#             return arguments_list
#         except FileNotFoundError as fNfE:
#             return create_error_message(error_type='file', message='Unable to obtain valid arguments',
#                                         error_message=str(fNfE))
#
#
#     def get_valid_options(self):
#         try:
#             options_list = {}
#             with open(self.options_list_path) as file:
#                 options_list.update(json.load(file))
#             return options_list
#         except FileNotFoundError as fNfE:
#             return create_error_message(error_type='file', message='Unable to obtain valid options',
#                                         error_message=str(fNfE))
#
#     def get_user_list(self):
#         try:
#             users_list = {}
#             with open(self.user_list_path) as file:
#                 users_list.update(json.load(file))
#             return users_list
#         except FileNotFoundError as fNfE:
#             return create_error_message(error_type='file', message='Unable to obtain user list',
#                                         error_message=str(fNfE))
#
#     def get_permissions_list(self):
#         try:
#             permissionss_list = {}
#             with open(self.permissions_list_path) as file:
#                 permissionss_list.update(json.load(file))
#             return permissionss_list
#         except FileNotFoundError as fNfE:
#             return create_error_message(error_type='file', message='Unable to obtain permissions list',
#                                         error_message=str(fNfE))
#         try:
#             for cmd in commands_from_file:
#                 if cmd == user_defined_command:
#                     return cmd, commands_from_file[cmd]
#                 else:
#                     raise IOError
#         except IOError as ioe:
#              return create_error_message(error_type='parse', message='Valid command not found', error_message=str(ioe))