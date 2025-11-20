import sqlite3
from .base_extractor import BaseExtractor

class SQLiteExtractor(BaseExtractor):
    def __init__(self, host=None, user=None, password=None, port=None, database="test_lab.db"):
        self.database = database
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.database)

    def extract_databases(self):
        return ["sqlite_local_lab"]

    def extract_tables(self, _=None):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cur.fetchall()]

    def extract_columns(self, _=None, table_name=None):
        cur = self.conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        return [(row[1], row[2]) for row in cur.fetchall()]

    def extract_storage(self):
        return []
