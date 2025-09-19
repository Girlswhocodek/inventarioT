from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    supervisor_id = Column(Integer, ForeignKey('empleados.id'))  # Relación de supervisión

    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    usuario = Column(String(50), nullable=False, unique=True)
    e_humano = Column(Integer, unique=True)
    area = Column(String(100))
    cargo = Column(String(100))
    
    # Relaciones
    user = relationship("User", back_populates="empleado", uselist=False)
    
    # Relación de supervisión: un empleado supervisa a muchos
    empleados_supervisados = relationship(
        "Empleado", 
        back_populates="supervisor",
        remote_side=[id]
    )

    # Relación de supervisión: un empleado es supervisado por uno
    supervisor = relationship(
        "Empleado", 
        back_populates="empleados_supervisados", 
        remote_side=[supervisor_id]
    )
    
    # Relación con Servidor (responsable) - CORREGIDO
    servidores_responsables = relationship(
        "Servidor", 
        back_populates="responsable_empleado",
        foreign_keys="[Servidor.responsable_id]"
    )

    # Relación con BaseDatos (administra)
    bases_datos_administradas = relationship(
        "BaseDatos", 
        back_populates="administrador"
    )

    # Relación con UsuarioBd (propietario)
    usuarios_bd_propietarios = relationship(
        "UsuarioBd",  
        back_populates="propietario"
    )

    def __repr__(self):
        return f"<Empleado(nombre='{self.nombre_completo}', cargo='{self.cargo}')>"
    
    def __str__(self):
        return self.nombre_completo