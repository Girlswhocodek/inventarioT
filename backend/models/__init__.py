from .base import Base, engine, get_db
from .servidor import Servidor
from .sistema_operativo import SistemaOperativo
from .base_datos import BaseDatos
from .gestor import Gestor

# Importar todos los modelos para que SQLAlchemy los detecte
__all__ = ['Base', 'engine', 'get_db', 'Servidor', 'SistemaOperativo', 'BaseDatos', 'Gestor']
EOL
