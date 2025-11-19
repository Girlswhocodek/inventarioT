from .postgres_extractor import PostgresExtractor
from .mysql_extractor import MySQLExtractor
from .oracle_extractor import OracleExtractor
from .sqlserver_extractor import SQLServerExtractor

def get_extractor(db_type: str, **kwargs):

    if db_type == "postgres":
        return PostgresExtractor(**kwargs)

    if db_type == "mysql":
        return MySQLExtractor(**kwargs)

    if db_type == "oracle":
        return OracleExtractor(**kwargs)

    if db_type == "sqlserver":
        return SQLServerExtractor(**kwargs)

    raise ValueError(f"Extractor no disponible para {db_type}")
