from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class RolBd(Base):
    __tablename__ = "roles_bd"

    id = Column(Integer, primary_key=True, index=True)
    base_datos_id = Column(Integer, ForeignKey('bases_datos.id'), nullable=False)
    
    nombre_rol = Column(String(100), nullable=False)
    permisos = Column(Text)  # JSON with permissions granted to the role
    fecha_creacion = Column(Date)
    estado = Column(String(20), default="activo")  # activo, inactivo
    
    
    base_datos = relationship(
        "BaseDatos", 
        back_populates="roles_bd"
    )

    usuarios = relationship(
        "UsuarioBd", 
        secondary="usuarios_roles", 
        back_populates="roles"
    )

    def __repr__(self):
        return f"<RolBd(nombre_rol='{self.nombre_rol}', base_datos_id={self.base_datos_id})>"

    def __str__(self):
        return self.nombre_rol