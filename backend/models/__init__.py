from models.base import Base, engine, get_db 
from models.servidor import Servidor
from models.sistema_operativo import SistemaOperativo
from models.base_datos import BaseDatos
from models.gestor import Gestor
from models.user import User

print("🔧 Creando todas las tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente!")
print("📁 Base de datos creada en: inventario.db")