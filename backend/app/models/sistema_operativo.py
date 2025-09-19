from sqlalchemy import Column, Date, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class SistemaOperativo(Base):
    __tablename__ = "sistemas_operativos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    distribucion = Column(String(50))  # Windows Server, Linux, etc.
    version = Column(String(20))
    tipo_usuario = Column(String(50))
    permisos = Column(JSON)  # Permisos como JSON: {"usuarios": [], "grupos": []}
    licencia = Column(String(100))
    estado = Column(String(20), default="activo") 
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    fecha_vencimiento = Column(Date)  # Fecha vencimiento de versión
    arquitectura = Column(String(20))  # x86, x64, ARM
    
    
    servidor_id = Column(Integer, ForeignKey('servidores.id'))
    
    # Relaciones
    servidor = relationship(
        "Servidor", 
        back_populates="sistemas_operativos"
    )
    
    def __repr__(self):
        return f"<SistemaOperativo(nombre='{self.nombre}', version='{self.version}')>"
    
    def __str__(self):
        return f"{self.nombre} {self.version}"
    
    def esta_activo(self):
        """Verifica si el sistema operativo está activo"""
        return self.estado.lower() == "activo"
    
    def esta_vigente(self):
        """Verifica si la versión del SO aún tiene soporte"""
        if self.fecha_vencimiento:
            from datetime import date
            return date.today() <= self.fecha_vencimiento
        return True 