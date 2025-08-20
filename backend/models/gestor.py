from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Gestor(Base):
    __tablename__ = "gestores"
    
    id = Column(Integer, primary_key=True, index=True)
    base_datos_id = Column(Integer, ForeignKey('bases_datos.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50))  # phpMyAdmin, pgAdmin, Enterprise Manager, etc.
    version = Column(String(20))
    permisos_asignados = Column(JSON)  # Permisos como JSON
    configuracion = Column(JSON)       # Configuración específica
    url_acceso = Column(String(200))
    estado = Column(String(20), default="activo")
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relación con la base de datos
    base_datos = relationship("BaseDatos", backref="gestores")
