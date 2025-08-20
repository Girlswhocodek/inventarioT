cat > backend/models/sistema_operativo.py << 'EOL'
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class SistemaOperativo(Base):
    __tablename__ = "sistemas_operativos"
    
    id = Column(Integer, primary_key=True, index=True)
    servidor_id = Column(Integer, ForeignKey('servidores.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    distribucion = Column(String(50))  # Windows Server, Linux, etc.
    version = Column(String(20))
    fecha_creacion = Column(DateTime)
    tipo_usuario = Column(String(50))
    permisos = Column(JSON)  # Permisos como JSON: {"usuarios": [], "grupos": []}
    licencia = Column(String(100))
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relación con el servidor
    servidor = relationship("Servidor", backref="sistemas_operativos")
EOL
