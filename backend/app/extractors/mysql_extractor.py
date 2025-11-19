import mysql.connector
from .base_extractor import BaseExtractor

class MySQLExtractor(BaseExtractor):
    def __init__(self, host, user, password, port=3306):
        self.conn_params = {
            "host": host,
            "user": user,
            "password": password,
            "port": port
        }
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(**self.conn_params)

    def extract_databases(self):
        cur = self.conn.cursor()
        cur.execute("SHOW DATABASES;")
        return [row[0] for row in cur.fetchall()]

    def extract_tables(self, database_name):
        cur = self.conn.cursor()
        cur.execute(f"USE {database_name};")
        cur.execute("SHOW TABLES;")
        return [row[0] for row in cur.fetchall()]

    def extract_columns(self, database_name, table_name):
        cur = self.conn.cursor()
        cur.execute(f"USE {database_name};")
        cur.execute(f"DESCRIBE {table_name};")
        return cur.fetchall()

    def extract_storage(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT table_schema,
                   SUM(data_length + index_length)/1024/1024 AS size_mb
            FROM information_schema.tables
            GROUP BY table_schema;
        """)
        return cur.fetchall()
