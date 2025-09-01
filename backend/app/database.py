# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import oracledb 

# carga de varia de entorno
load_dotenv()

# confi driver de Oracle
# print(f"🐍 Using oracledb version: {oracledb.__version__}")  

def get_database_engine():
    use_sqlite = os.getenv("USE_SQLITE", "True").lower() == "true"
    
    if use_sqlite:
        # SQLite
        sqlite_url = "sqlite:///./inventario.db"
        print("📁 Usando SQLite para desarrollo: inventario.db")
        return create_engine(
            sqlite_url, 
            connect_args={"check_same_thread": False},
            echo=True 
        )
    else:
        # Oracle
        oracle_user = os.getenv("ORACLE_USER")
        oracle_password = os.getenv("ORACLE_PASSWORD")
        oracle_host = os.getenv("ORACLE_HOST")
        oracle_port = os.getenv("ORACLE_PORT", "1521")
        oracle_service = os.getenv("ORACLE_SERVICE", "XEPDB1")
        
        if not all([oracle_user, oracle_password, oracle_host]):
            raise ValueError("❌ Configuración de Oracle incompleta en variables de entorno")
        
        # Cadena de conexión para Oracle usando el driver oracledb
        oracle_url = f"oracle+oracledb://{oracle_user}:{oracle_password}@{oracle_host}:{oracle_port}/?service_name={oracle_service}"
        
        print("🗄️ Usando Oracle Database")
        print(f"   Host: {oracle_host}:{oracle_port}")
        print(f"   Service: {oracle_service}")
        print(f"   User: {oracle_user}")
        
        return create_engine(
            oracle_url,
            echo=True,  
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
        )

#basic
engine = get_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency para obtener la sesión de la bd.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#verificar
def test_connection():
    """
    Función para probar la conexión a la base de datos.
    """
    try:
        with engine.connect() as conn:
            if engine.url.get_backend_name() == "sqlite":
                result = conn.execute("SELECT 'SQLite connection successful' as status")
            else:
                result = conn.execute("SELECT 'Oracle connection successful' as status FROM dual")
            print(f"✅ {result.scalar()}")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False