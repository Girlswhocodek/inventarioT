import database
from .postgres_extractor import PostgresExtractor
from .mysql_extractor import MySQLExtractor
from .oracle_extractor import OracleExtractor 
from .sqlserver_extractor import SQLServerExtractor
from .sqlite_extractor import SQLiteExtractor

def get_extractor(db_type: str):
    db_type = db_type.lower()

    if db_type == "mysql":
        try:
            from .mysql_extractor import MySQLExtractor
            return MySQLExtractor()
        except ImportError:
            raise RuntimeError("Para usar MySQL debes instalar: pip install mysql-connector-python")

    elif db_type == "postgres":
        try:
            from .postgres_extractor import PostgresExtractor
            return PostgresExtractor()
        except ImportError:
            raise RuntimeError("Para usar PostgreSQL debes instalar: pip install psycopg2-binary")

    elif db_type == "mssql":
        try:
            from .mssql_extractor import MSSQLExtractor
            return MSSQLExtractor()
        except ImportError:
            raise RuntimeError("Para usar SQL Server debes instalar: pip install pyodbc")

    elif db_type == "oracle":
        try:
            from .oracle_extractor import OracleExtractor
            return OracleExtractor()
        except ImportError:
            raise RuntimeError("Para usar Oracle debes instalar: pip install cx_Oracle y Oracle Instant Client")
    elif db_type == "sqlite": 
        
        if not database:
            raise ValueError("SQLite requiere el parámetro 'database' (ruta del archivo).")
        try:  
            return SQLiteExtractor(database=database) 
        except ImportError:
            raise RuntimeError("La clase SQLiteExtractor no se encuentra en la ruta esperada.")

    else:
        raise ValueError(f"Tipo de base de datos no soportado: {db_type}")
    
    

