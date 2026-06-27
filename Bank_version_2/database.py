import mysql.connector
from mysql.connector import Error
import config


class Database:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    # -----------------------------
    # Connect
    # -----------------------------

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=config.HOST,
                user=config.USER,
                password=config.PASSWORD,
                database=config.DATABASE,
                autocommit=False   # implicit transaction on every execute()
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to MySQL successfully.")
        except Error as e:
            print("Database Connection Error")
            print(e)

    # -----------------------------
    # Execute INSERT/UPDATE/DELETE
    # -----------------------------

    def execute(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            print(e)
            return False

    # -----------------------------
    # SELECT ONE ROW
    # -----------------------------

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    # -----------------------------
    # SELECT MANY ROWS
    # -----------------------------

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    # -----------------------------
    # Close
    # -----------------------------

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    # -----------------------------------
    # Begin Transaction
    # -----------------------------------

    def begin_transaction(self):
        # With autocommit=False the connection is already in a transaction.
        # start_transaction() would raise an error here, so we do nothing.
        pass

    # -----------------------------------
    # Commit
    # -----------------------------------

    def commit(self):
        self.connection.commit()

    # -----------------------------------
    # Rollback
    # -----------------------------------

    def rollback(self):
        self.connection.rollback()