from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class BaseDatos(Base):
    __tablename__ = "bases_datos"
    
    id = Column(Integer, primary_key=True, index=True)
    sistema_operativo_id = Column(Integer, ForeignKey('sistemas_operativos.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    motor = Column(String(50))  # MySQL, PostgreSQL, Oracle, etc.
    version = Column(String(20))
    fecha_inicio = Column(DateTime)
    responsable = Column(String(100))
    espacio_gb = Column(Float)  # Espacio que ocupa en GB
    objetos = Column(Integer)   # Número de objetos (tablas, procedures, etc.)
    puerto = Column(Integer)
    estado = Column(String(20), default="activo")
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relación con el sistema operativo
    sistema_operativo = relationship("SistemaOperativo", backref="bases_datos")
