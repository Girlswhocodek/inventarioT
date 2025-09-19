from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class UsuarioBd(Base):
    __tablename__ = "usuarios_bd"
    
    id = Column(Integer, primary_key=True, index=True)
    base_datos_id = Column(Integer, ForeignKey('bases_datos.id'), nullable=False)
    propietario_id = Column(Integer, ForeignKey('empleados.id'))  # AGREGADO
    
    nombre_usuario = Column(String(100), nullable=False)
    permisos = Column(Text)  # JSON con permisos: {"select": ["tabla_a", "vista_b"]}
    fecha_creacion = Column(Date)
    estado = Column(String(20), default="activo")  # activo, inactivo
    
    # Relaciones - CORREGIDAS
    base_datos = relationship(
        "BaseDatos", 
        back_populates="usuarios_bd"
    )
    
    propietario = relationship(
        "Empleado", 
        back_populates="usuarios_bd_propietarios",
        foreign_keys=[propietario_id]
    )
    
    roles = relationship(
        "RolBd", 
        secondary="usuarios_roles", 
        back_populates="usuarios"
    )
    
    def __repr__(self):
        return f"<UsuarioBd(nombre='{self.nombre_usuario}', base_datos_id={self.base_datos_id})>"

    def __str__(self):
        return self.nombre_usuario