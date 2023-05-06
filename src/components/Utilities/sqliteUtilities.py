import sqlite3 as sql
from utilities import create_error_message
from sqlite3 import Error
from pathlib import Path


class SqliteUtilities:

    def __init__(self):
        self.db_name = None
        self.db_path = None
        self.connection = None
        self.connection_open = False

    def set_db_name(self, name):
        if not name.endswith('.db'):
            self.db_name = f'{name}_database.db'
        else:
            self.db_name = name

    def set_db_path(self, path):
        if not Path(path).exists():
            self.db_path = Path(__file__).parent.parent.parent.joinpath(f'data/database/{Path(path).root}')
        else:
            self.db_path = path

    def set_connection(self, db_path):
        self.connection = sql.connect(db_path)

    def set_connection_open(self, status):
        self.connection_open = status

    def get_db_name(self):
        return self.db_name

    def get_db_path(self):
        return self.db_path

    def get_connection(self):
        return self.connection

    def establish_connection(self, path, name):
        try:
            self.set_db_name(name)
            self.set_db_path(path)
            self.set_connection(self.get_db_path())
            self.set_connection_open(True)
            print(sql.version, '\nConnection Successful')
            return self.get_connection()
        except Error as e:
            create_error_message(error_type='Database Connection Error:', message='Unable to establish connection',
                                 error_message=f'{e}')

    def close_connection(self):
        try:
            if self.connection:
                self.connection.close()
        except Error as e:
            create_error_message(error_type='Database Connection Error:', message='Unable to close connection',
                                 error_message=f'{e}')

    def create_tables(self, tables):
        try:
            for table_command in tables:
                self.connection.cursor().execute(table_command)
        except Error as e:
            create_error_message(error_type='Database CRUD Error:', message=f'Unable to create {tables}',
                                 error_message=f'{e}')
        finally:
            if self.connection_open:
                self.close_connection()

    def create_initial_tables(self, path, table_list, name=None):
        try:
            conn = self.establish_connection(path, name)
            while conn is not None:
                self.create_tables(table_list)
        except Error as e:
            create_error_message(error_type='Database CRUD Error:', message=f'Unable to create {table_list}',
                                 error_message=f'{e}')
        finally:
            if self.connection_open:
                self.close_connection()
