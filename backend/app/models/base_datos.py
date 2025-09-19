from sqlalchemy import Column, Integer, Numeric, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class BaseDatos(Base):
    __tablename__ = "bases_datos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    motor = Column(String(50))  # MySQL, PostgreSQL, Oracle, etc.
    version = Column(String(20))
    fecha_inicio = Column(DateTime)
    responsable = Column(String(100))
    espacio_gb = Column(Float)  # Espacio que ocupa en GB
    objetos = Column(Integer)   # Número de objetos (tablas, procedures, etc.)
    puerto = Column(Integer)
    estado = Column(String(20), default="online")
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    espacio_total_gb = Column(Numeric(15,2))  
    espacio_objetos_gb = Column(Numeric(15,2))  
    permisos_asignados = Column(Text)  # JSON con permisos asignados
    dblinks = Column(Text)
    caracter_set = Column(String(50))
    nls_characterset = Column(String(50))
    fecha_creacion = Column(DateTime, default=func.now())
    
    # Foreign Keys - CORREGIDAS
    instancia_bd_id = Column(Integer, ForeignKey('instancias_bd.id'), nullable=False)
    administrador_id = Column(Integer, ForeignKey('empleados.id'))
    
    # Relaciones - CORREGIDAS
    roles_bd = relationship(
        "RolBd",
        back_populates="base_datos"
    )
    instancia_bd = relationship(
        "InstanciaBd", 
        back_populates="bases_datos"
    )
    
    administrador = relationship(
        "Empleado", 
        back_populates="bases_datos_administradas",
        foreign_keys=[administrador_id]
    )
    
    objetos_bd = relationship(
        "ObjetoBd", 
        back_populates="base_datos", 
        cascade="all, delete-orphan"
    )
    
    usuarios_bd = relationship(
        "UsuarioBd", 
        back_populates="base_datos", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<BaseDatos(nombre='{self.nombre}', motor='{self.motor}')>"
    
    def __str__(self):
        return self.nombre
    
    @property
    def url_conexion(self):
        """Genera URL de conexión usando la instancia"""
        if self.instancia_bd:
            return self.instancia_bd.url_conexion
        return f"localhost:{self.puerto}" if self.puerto else "localhost"
    
    @property
    def porcentaje_uso_espacio(self):
        """Calcula el porcentaje de uso del espacio"""
        if self.instancia_bd and self.instancia_bd.espacio_asignado_gb and self.espacio_total_gb:
            instancia_espacio = float(self.instancia_bd.espacio_asignado_gb)
            bd_espacio = float(self.espacio_total_gb)
            return round((bd_espacio / instancia_espacio) * 100, 2)
        return 0
    
    def esta_online(self):
        """Verifica si la base de datos está online"""
        return self.estado.lower() == "online"