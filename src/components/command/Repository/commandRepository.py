from src.components.command.Models.Commands.commands import Command
from src.components.Utilities.sqliteUtilities import SqliteUtilities


class CommandRepository:

    def __init__(self):
        self.command = Command(None)
        self.initial_sql = SqliteUtilities()
        self.database_path = None

    def create_command_object(self, command_name, command_arguments, command_options, command_type):
        return self.command.create_command_object(command_name, command_arguments, command_options, command_type)

    def create_initial_tables(self):
        table_list = self.command_table(), self.arguments_table(), self.options_table()
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

    @staticmethod
    def command_table():
        command_table = """
        CREATE TABLE IF NOT EXISTS Commands (
        id INTEGER AUTOINCREMENT PRIMARY KEY,
        command_name TEXT,
        command_arguments TEXT,
        command_options TEXT,
        command_type TEXT)
        """
        return command_table

    @staticmethod
    def arguments_table():
        arguments_table = """
        CREATE TABLE IF NOT EXISTS Arguments (
        command_id INTEGER AUTOINCREMENT,
        command_arguments TEXT),
        FOREIGN KEY (command_id) REFERENCES Commands(id)
        """
        return arguments_table

    @staticmethod
    def options_table():
        options_table = """
        CREATE TABLE IF NOT EXISTS Options (
        command_id INTEGER AUTOINCREMENT,
        command_options TEXT),
        FOREIGN KEY (command_id) REFERENCES Commands(id)
        """
        return options_table

    @staticmethod
    def help_command_table():
        help_table = """
        CREATE TABLE IF NOT EXISTS Help (
        id INTEGER AUTOINCREMENT,
        command_info TEXT,
        arguments_info TEXT,
        options_info TEXT,
        type_info TEXT),
        FOREIGN KEY (id) REFERENCES Commands(id)
        """
        return help_table


