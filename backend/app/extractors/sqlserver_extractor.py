try:
    import pyodbc
except ImportError:
    pyodbc = None  # Permite cargar el archivo aunque pyodbc no esté instalado

from .base_extractor import BaseExtractor


class SQLServerExtractor(BaseExtractor):
    def __init__(self, host, user, password, database, port=1433):
        if pyodbc is None:
            raise RuntimeError(
                "pyodbc no está instalado.\n"
                "Instálalo con: pip install pyodbc\n"
                "Además necesitas un driver ODBC para SQL Server."
            )

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None

    def connect(self):
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={self.host},{self.port};"
            f"DATABASE={self.database};"
            f"UID={self.user};"
            f"PWD={self.password}"
        )
        self.conn = pyodbc.connect(connection_string)

    def extract_databases(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        return [row[0] for row in cursor.fetchall()]

    def extract_tables(self, database_name):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT TABLE_NAME 
            FROM {database_name}.INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        return [row[0] for row in cursor.fetchall()]

    def extract_columns(self, database_name, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM {database_name}.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
        """, (table_name,))
        return cursor.fetchall()

    def extract_storage(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                t.NAME AS table_name,
                SUM(a.total_pages) * 8 AS total_space_kb
            FROM sys.tables t
            INNER JOIN sys.indexes i ON t.object_id = i.object_id
            INNER JOIN sys.partitions p ON i.object_id = p.object_id 
                AND i.index_id = p.index_id
            INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            GROUP BY t.NAME
        """)
        return cursor.fetchall()
