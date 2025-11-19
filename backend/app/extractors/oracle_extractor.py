import cx_Oracle
from .base_extractor import BaseExtractor

class OracleExtractor(BaseExtractor):
    def __init__(self, host, user, password, port=1521, service="XE"):
        self.dsn = cx_Oracle.makedsn(host, port, service_name=service)
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        self.conn = cx_Oracle.connect(self.user, self.password, self.dsn)

    def extract_databases(self):
        return ["DEFAULT_ORACLE_DB"]

    def extract_tables(self, _):
        cur = self.conn.cursor()
        cur.execute("SELECT table_name FROM user_tables")
        return [row[0] for row in cur.fetchall()]

    def extract_columns(self, _, table_name):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT column_name, data_type 
            FROM user_tab_columns
            WHERE table_name = :t
        """, {"t": table_name.upper()})
        return cur.fetchall()

    def extract_storage(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT segment_type, SUM(bytes)/1024/1024 AS size_mb
            FROM user_segments
            GROUP BY segment_type
        """)
        return cur.fetchall()
