import pyodbc
from .base_extractor import BaseExtractor

class SQLServerExtractor(BaseExtractor):
    def __init__(self, host, user, password, database="master"):
        self.conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={host};"
            f"UID={user};"
            f"PWD={password};"
            f"DATABASE={database}"
        )
        self.conn = None

    def connect(self):
        self.conn = pyodbc.connect(self.conn_str)

    def extract_databases(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sys.databases")
        return [row[0] for row in cur.fetchall()]

    def extract_tables(self, database_name):
        cur = self.conn.cursor()
        cur.execute(f"USE {database_name}")
        cur.execute("SELECT name FROM sys.tables")
        return [row[0] for row in cur.fetchall()]

    def extract_columns(self, database_name, table_name):
        cur = self.conn.cursor()
        cur.execute(f"USE {database_name}")
        cur.execute(f"""
            SELECT name, system_type_id 
            FROM sys.columns 
            WHERE object_id = OBJECT_ID('{table_name}')
        """)
        return cur.fetchall()

    def extract_storage(self):
        cur = self.conn.cursor()
        cur.execute("EXEC sp_spaceused;")
        return cur.fetchall()
