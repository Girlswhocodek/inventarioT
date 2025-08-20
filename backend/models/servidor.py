from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base

class Servidor(Base):
    __tablename__ = "servidores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    ip = Column(String(15), nullable=False)
    cpu_nucleos = Column(Integer)
    ram_gb = Column(Integer)
    almacenamiento_gb = Column(Integer)
    estado = Column(String(20), default="activo")
    responsable = Column(String(100))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
