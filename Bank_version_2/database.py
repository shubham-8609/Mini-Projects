import os
import mysql.connector
from mysql.connector import Error
import config


class Database:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.setup()

    # -----------------------------
    # Setup — create DB if missing,
    # then connect to it
    # -----------------------------

    def setup(self):
        try:
            # Step 1 — connect to MySQL server only (no database selected)
            server_conn = mysql.connector.connect(
                host=config.HOST,
                user=config.USER,
                password=config.PASSWORD,
                autocommit=True
            )
            server_cursor = server_conn.cursor()

            # Step 2 — check if the database already exists
            server_cursor.execute(
                "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA "
                "WHERE SCHEMA_NAME = %s",
                (config.DATABASE,)
            )
            db_exists = server_cursor.fetchone() is not None

            # Step 3 — run setup script only when database is absent
            if not db_exists:
                print(f"Database '{config.DATABASE}' not found. Running setup...")
                self._run_sql_script(server_cursor, config.SQL_FILE)
                print(f"Database '{config.DATABASE}' created successfully.")
            else:
                print(f"Database '{config.DATABASE}' already exists. Skipping setup.")

            server_cursor.close()
            server_conn.close()

        except Error as e:
            print("Setup Error:", e)
            return

        # Step 4 — reconnect with the database selected
        self.connect()

    # -----------------------------
    # Run SQL script file
    # -----------------------------

    def _run_sql_script(self, cursor, sql_file):
        # Resolve path relative to this file so it works from any working directory
        sql_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            sql_file
        )

        if not os.path.exists(sql_path):
            raise FileNotFoundError(f"SQL file not found: {sql_path}")

        with open(sql_path, "r", encoding="utf-8") as f:
            raw = f.read()

        # Remove full-line comments (lines starting with --)
        lines = [
            line for line in raw.splitlines()
            if not line.strip().startswith("--")
        ]
        cleaned = "\n".join(lines)

        # Split on semicolons, skip empty results
        statements = [
            stmt.strip()
            for stmt in cleaned.split(";")
            if stmt.strip()
        ]

        for stmt in statements:
            try:
                cursor.execute(stmt)
            except Error as e:
                print(f"SQL Error in statement:\n{stmt}\n→ {e}")
                raise

    # -----------------------------
    # Connect to the database
    # -----------------------------

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=config.HOST,
                user=config.USER,
                password=config.PASSWORD,
                database=config.DATABASE,
                autocommit=False
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to MySQL successfully.")
        except Error as e:
            print("Database Connection Error:", e)

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
    # Begin Transaction (no-op)
    # autocommit=False keeps us in an
    # implicit transaction at all times
    # -----------------------------------

    def begin_transaction(self):
        pass

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()