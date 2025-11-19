import psycopg2 # type: ignore
from .base_extractor import BaseExtractor

class PostgresExtractor(BaseExtractor):
    def __init__(self, host, user, password, port=5432):
        self.conn_params = {
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "dbname": "postgres"
        }
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(**self.conn_params)

    def extract_databases(self):
        cur = self.conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        return [row[0] for row in cur.fetchall()]

    def extract_tables(self, database_name: str):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public';
        """)
        return [row[0] for row in cur.fetchall()]

    def extract_columns(self, database_name: str, table_name: str):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s;
        """, (table_name,))
        return cur.fetchall()

    def extract_storage(self):
        cur = self.conn.cursor()
        cur.execute("SELECT pg_size_pretty(pg_database_size('postgres'));")
        return cur.fetchone()[0]
