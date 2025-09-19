from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class InstanciaBd(Base):
    __tablename__ = "instancias_bd"
    
    id = Column(Integer, primary_key=True, index=True)
    servidor_id = Column(Integer, ForeignKey('servidores.id'), nullable=False)
    gestor_bd_id = Column(Integer, ForeignKey('gestores.id'), nullable=False)  # MANTENER ESTE
    nombre_instancia = Column(String(100), nullable=False)
    puerto = Column(Integer)
    fecha_instalacion = Column(Date)
    parametros_bd = Column(Text)
    cantidad_sesiones = Column(Integer)
    espacio_asignado_gb = Column(Numeric(15,2))
    unidades_disco = Column(Text)
    lista_perfiles = Column(Text)
    estado = Column(String(20), default="activo")
    

    # Campos de auditoría del sistema
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones - CORREGIDAS
    servidor = relationship(
        "Servidor", 
        back_populates="instancias_bd"
    )
    
    gestor = relationship(
        "Gestor", 
        back_populates="instancias",
        foreign_keys=[gestor_bd_id]
    )
    
    bases_datos = relationship(
        "BaseDatos", 
        back_populates="instancia_bd", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<InstanciaBd(nombre='{self.nombre_instancia}', puerto={self.puerto}, servidor_id={self.servidor_id})>"
    
    def __str__(self):
        return f"{self.nombre_instancia}:{self.puerto}"
    
    @property
    def url_conexion(self):
        """Genera una URL básica de conexión"""
        if self.servidor and self.servidor.ip_address:
            return f"{self.servidor.ip_address}:{self.puerto}"
        return f"localhost:{self.puerto}"
    
    @property
    def espacio_usado_gb(self):
        """Calcula el espacio usado por todas las bases de datos de esta instancia"""
        if self.bases_datos:
            return sum(float(bd.espacio_total_gb or 0) for bd in self.bases_datos)
        return 0
    
    @property
    def espacio_libre_gb(self):
        """Calcula el espacio libre disponible"""
        if self.espacio_asignado_gb:
            return float(self.espacio_asignado_gb) - self.espacio_usado_gb
        return 0
    
    @property
    def porcentaje_uso(self):
        """Calcula el porcentaje de uso del espacio"""
        if self.espacio_asignado_gb and self.espacio_asignado_gb > 0:
            return round((self.espacio_usado_gb / float(self.espacio_asignado_gb)) * 100, 2)
        return 0
    
    def esta_activa(self):
        """Verifica si la instancia está activa"""
        return self.estado.lower() == "activo"
    
    def get_numero_bases_datos(self):
        """Retorna el número de bases de datos en esta instancia"""
        return len(self.bases_datos) if self.bases_datos else 0