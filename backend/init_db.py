from models import Base, engine
from models.servidor import Servidor
from models.sistema_operativo import SistemaOperativo
from models.base_datos import BaseDatos
from models.gestor import Gestor
from models.user import User

# Forzar creación de tablas
Base.metadata.create_all(bind=engine)
print("✅ Todas las tablas creadas exitosamente")
