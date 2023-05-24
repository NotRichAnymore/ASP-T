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
                print(e)

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
            self.db_name = 'aspt'
        except (Exception, Error) as e:
            return e

    def create_database(self):
        try:
            create_db_query = """
            CREATE DATABASE IF NOT EXISTS ASPT;
            """
            with MySQLUtilities.connection.cursor() as cursor:
                cursor.execute(create_db_query)
        except (Exception, Error) as e:
            return e
        finally:
            cursor.close()

    def show_all_databases(self):
        try:
            with MySQLUtilities.connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                return cursor.fetchall()
        except (Exception, Error) as e:
            return e
        finally:
            cursor.close()

    def create_users_table(self):
        try:
            table_query = """
            CREATE TABLE IF NOT EXISTS ASPT.users (
              id INT AUTO_INCREMENT PRIMARY KEY,
              username VARCHAR(16) NOT NULL,
              hashed_password CHAR(60) NOT NULL,
              transaction_time TIMESTAMP NOT NULL,
            );
            """
            with MySQLUtilities.connection.cursor() as cursor:
                cursor.execute(table_query)
                MySQLUtilities.connection.commit()
        except Error as e:
            return e
        finally:
            cursor.close()


    def insert_into_users_table(self, username, hashed_password):
        try:
            update_query = f"""
            INSERT INTO ASPT.users (username, hashed_password, transaction_time)
            VALUES (%s, %s, %s)
            """
            timestamp = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S')
            values = (username, hashed_password, timestamp)
            with MySQLUtilities.connection.cursor() as cursor:
                cursor.execute(update_query, values)
                MySQLUtilities.connection.commit()
        except Error as e:
            return e


    @staticmethod
    def get_all_users():
        try:
            query = """
            SELECT users.username FROM users;
            """
            with MySQLUtilities.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            return e
        finally:
            cursor.close()

    @staticmethod
    def get_last_entry():
        try:
            query = """
            SELECT MAX(transaction_time)
            FROM users.transaction_time;
            """
            with MySQLUtilities.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            return e
        finally:
            cursor.close()

    def delete_user(self, username, hashed_password):
        try:
            delete_query = """
            DELETE FROM users
            WHERE users.name = %s AND users.hashed_password = %s
            ORDER BY users.id DESC;
            """
            values = (username, hashed_password)
            with self.cursor as cursor:
                cursor.execute(delete_query, values)
                self.connection.commit()
        except Error as e:
            return e
        finally:
            cursor.close()

    def get_user_by_name(self, username):
        try:
            query = """
            SELECT users.name FROM users
            WHERE users.name = %s
            ORDER BY users.id DESC;
            """
            with self.cursor as cursor:
                cursor.execute(query, username)
        except Error as e:
            return e
        finally:
            cursor.close()

    def get_user_by_id(self, user_id):
        try:
            query = f"""
            SELECT users.name FROM users
            WHERE users.id = %s
            ORDER BY users.id DESC;
            """
            with self.cursor as cursor:
                cursor.execute(query, user_id)
        except Error as e:
            return e
        finally:
            cursor.close()


