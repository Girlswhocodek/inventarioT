from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class ObjetoBd(Base):
    __tablename__ = "objetos_bd"
    
    id = Column(Integer, primary_key=True, index=True)
    base_datos_id = Column(Integer, ForeignKey('bases_datos.id'), nullable=False)
    
    nombre = Column(String(128), nullable=False)
    tipo = Column(String(30), nullable=False)  # tabla, vista, procedimiento, funcion, trigger, indice, etc.
    esquema = Column(String(50))  # Para Oracle/PostgreSQL
    descripcion = Column(Text)
    
    tamaño_kb = Column(Numeric(15,2))
    num_registros = Column(Integer)  # Para tablas
    
    # Fechas
    fecha_modificacion = Column(DateTime) 
    fecha_registro = Column(DateTime, default=func.now())  # Fecha de registro en sistema
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Estado y metadatos
    estado = Column(String(20), default="activo")  # activo, inactivo, obsoleto
    comentarios = Column(Text)
    dependencias = Column(Text)  # JSON con objetos de los que depende
    
    # Información específica por tipo de objeto
    parametros = Column(Text)  # Para procedimientos y funciones (JSON)
    columnas = Column(Text)  # Para tablas y vistas (JSON)
    indices = Column(Text)  # Para tablas (JSON)
    
    # Relaciones
    base_datos = relationship("BaseDatos", back_populates="objetos_bd")
    
    def __repr__(self):
        return f"<ObjetoBd(nombre='{self.nombre}', tipo='{self.tipo}', base_datos_id={self.base_datos_id})>"
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo incluyendo esquema si existe"""
        if self.esquema:
            return f"{self.esquema}.{self.nombre}"
        return self.nombre
    
    @property
    def tamaño_mb(self):
        """Retorna el tamaño en MB"""
        if self.tamaño_kb:
            return float(self.tamaño_kb) / 1024
        return 0
    
    @property
    def tamaño_gb(self):
        """Retorna el tamaño en GB"""
        if self.tamaño_kb:
            return float(self.tamaño_kb) / (1024 * 1024)
        return 0
    
    def es_tabla(self):
        """Verifica si el objeto es una tabla"""
        return self.tipo.lower() == 'tabla'
    
    def es_vista(self):
        """Verifica si el objeto es una vista"""
        return self.tipo.lower() == 'vista'
    
    def es_procedimiento(self):
        """Verifica si el objeto es un procedimiento almacenado"""
        return self.tipo.lower() in ['procedimiento', 'procedure']
    
    def es_funcion(self):
        """Verifica si el objeto es una función"""
        return self.tipo.lower() in ['funcion', 'function']
    
    def es_trigger(self):
        """Verifica si el objeto es un trigger"""
        return self.tipo.lower() == 'trigger'
    
    def es_indice(self):
        """Verifica si el objeto es un índice"""
        return self.tipo.lower() in ['indice', 'index']