# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from pathlib import Path


class Database:
    """
    PostgreSQL database handler class for Flask apps.
    Keeps connection and cursor internally, provides simple query methods.
    """

    def __init__(self, app=None):
        self.conn = None
        self.cursor = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the DB connection using Flask app config."""
        try:
            self.conn = psycopg2.connect(
                host=app.config.get("DB_HOST", "localhost"),
                database=app.config.get("DB_NAME", "flaskrest"),
                user=app.config.get("DB_USER", "postgres"),
                password=app.config.get("DB_PASSWORD", "12345"),
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute(
                """
            SELECT * from public.items
        """
            )
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)

            print("✅ PostgreSQL database connected successfully.")
        except Exception as e:
            print(f"❌ Failed to connect to PostgreSQL: {e}")
            self.conn, self.cursor = None, None

    def execute_query(self, query, params=None, fetch=False):
        """Execute a query safely."""
        if not self.conn or not self.cursor:
            raise ConnectionError("Database not initialized or connection lost.")
        try:
            self.cursor.execute(query, params or ())
            if fetch:
                return self.cursor.fetchall()
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Query execution failed: {e}")
            raise e

    def close(self):
        """Close DB connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("🔒 Database connection closed.")
        except Exception as e:
            print(f"⚠️ Error closing DB connection: {e}")

    def read_all(self, filename, params=None):
        # Get directory where database.py is located
        current_dir = Path(__file__).resolve().parent
        sql_file = current_dir / "queries" / filename
        try:
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_script = f.read()
                print(sql_script)
        except Exception as e:
            print(f"Error reading SQL file {filename}: {e}")
        try:
            self.cursor.execute(sql_script, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error reading SQL file {filename}: {e}")
            raise e

    def insert_many(self, filename, items=None):

        # Get directory where database.py is located
        current_dir = Path(__file__).resolve().parent
        sql_file = current_dir / "queries" / filename
        try:
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_script = f.read()
                print(f"sql_script =>{sql_script}")
        except Exception as e:
            print(f"Error reading SQL file {filename}: {e}")

        try:

            self.cursor.executemany(sql_script, items)
            self.conn.commit()
            return "success"
        except Exception as e:
            print(f"Error executing the command")
            raise e
