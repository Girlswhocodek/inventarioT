from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Servidor(Base):
    __tablename__ = "servidores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    tecnologia = Column(String(20))
    particionado = Column(Boolean, default=False)
    cpu_nucleos = Column(Integer)
    ram_gb = Column(Numeric(10,2))
    almacenamiento_gb = Column(Integer)
    fecha_instalacion_so = Column(Date)
    ip = Column(String(15))
    fabricante = Column(String(50))  # Dell, HP, IBM
    modelo = Column(String(50))
    numero_serie = Column(String(100))
    ubicacion = Column(String(100))
    estado = Column(String(20), default="activo")
    responsable = Column(String(100))  # Campo de texto - MANTENER
    arquitectura = Column(String(20))  # x86, x64, ARM
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

    # Foreign Key para el responsable empleado - CORREGIDO
    responsable_id = Column(Integer, ForeignKey('empleados.id'))
    
    # Relaciones - CORREGIDAS
    responsable_empleado = relationship(
        "Empleado", 
        back_populates="servidores_responsables",
        foreign_keys=[responsable_id]
    )
    
    instancias_bd = relationship(
        "InstanciaBd", 
        back_populates="servidor"
    )
    
    sistemas_operativos = relationship(
        "SistemaOperativo", 
        back_populates="servidor", 
        cascade="all, delete-orphan"
    )
    
    discos = relationship(
        "Disco", 
        back_populates="servidor", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Servidor(nombre='{self.nombre}', ip='{self.ip_address}')>"
    
    def __str__(self):
        return self.nombre