import datetime

from mysql.connector import connect, Error
import pysnooper


@pysnooper.snoop()
class MySQLUtilities:

    connection = None
    cursor = None

    def __init__(self, host, username, password, database=None):
        self.hostname = host
        self.username = username
        self.password = password
        self.db_name = database

        if not MySQLUtilities.connection:
            try:
                MySQLUtilities.connection = connect(user=self.username, password=self.password,
                                                    host=self.hostname, database='aspt')
            except Error as e:
                MySQLUtilities.connection = connect(user=self.username, password=self.password,
                                                    host=self.hostname)

    def set_hostname(self, host):
        self.hostname = host

    def set_username(self, user):
        self.username = user

    def set_password(self, password):
        self.password = password

    def set_db_name(self, database_name):
        self.db_name = database_name

    def close_connection(self):
        try:
            MySQLUtilities.connection.close()
        except (Exception, Error) as e:
            raise e

    def initialise_db(self, program_user, pu_password):
        try:
            self.create_database()
            self.create_users_table()
            self.insert_into_users_table(program_user, pu_password)
            MySQLUtilities.connection.close()
            MySQLUtilities.connection = connect(user=self.username, password=self.password,
                                                host=self.hostname, database='aspt')
        except (Exception, Error) as e:
            return e

    def create_database(self):
        try:
            create_db_query = """
            CREATE DATABASE IF NOT EXISTS ASPT;
            """
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(create_db_query)
        except (Exception, Error) as e:
            return e
        

    def show_all_databases(self):
        try:
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute("SHOW DATABASES")
            return cursor.fetchall()
        except (Exception, Error) as e:
            return e
        

    def create_users_table(self):
        try:
            table_query = """
            CREATE TABLE IF NOT EXISTS ASPT.users (
              id INT AUTO_INCREMENT PRIMARY KEY,
              username VARCHAR(16) UNIQUE NOT NULL,
              hashed_password CHAR(60) UNIQUE NOT NULL,
              transaction_time DATETIME NOT NULL
            );
            """
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(table_query)
            MySQLUtilities.connection.commit()
        except Error as e:
            return e
        


    def insert_into_users_table(self, username, hashed_password):
        try:
            update_query = f"""
            INSERT INTO ASPT.users (username, hashed_password, transaction_time)
            VALUES (%s, %s, %s)
            """
            current_time = str(datetime.datetime.now().time())
            parsed_time = [current_time[:current_time.index(ele)] for ele in current_time if ele == '.']
            timestamp = f"{str(datetime.datetime.now().date())} {''.join(parsed_time)}"

            values = (username, hashed_password, timestamp)
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(update_query, values)
            MySQLUtilities.connection.commit()
        except Error as e:
            return e

    @staticmethod
    @pysnooper.snoop()
    def get_all_users():
        try:
            query = """
            SELECT users.username FROM users;
            """
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            return e
        
    @staticmethod
    @pysnooper.snoop()
    def get_last_entry():
        try:
            query = """
            SELECT username, hashed_password
            FROM aspt.users
            GROUP BY id
            ORDER BY transaction_time DESC
            LIMIT 1;
            """
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            return e
        

    def delete_user(self, username, hashed_password):
        try:
            delete_query = """
            DELETE FROM users
            WHERE users.name = %s AND users.hashed_password = %s
            ORDER BY users.id DESC;
            """
            values = (username, hashed_password)
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(delete_query, values)
            MySQLUtilities.connection.commit()
        except Error as e:
            return e
        

    def get_user_by_name(self, username):
        try:
            query = """
            SELECT username FROM aspt.users
            WHERE users.username = %(users.username)s;  
            """
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(query, {'users.username': username})
            return cursor.fetchall()
        except Error as e:
            return e
        

    def get_user_by_id(self, user_id):
        try:
            query = f"""
            SELECT username FROM aspt.users
            WHERE users.id = %(users.id)s;
            """
            cursor = MySQLUtilities.connection.cursor()
            cursor.execute(query, {'users.id': user_id})
            return cursor.fetchall()
        except Error as e:
            return e
        


