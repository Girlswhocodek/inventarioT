from sqlalchemy import Column, Date, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Gestor(Base):
    __tablename__ = "gestores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)  # Oracle, MySQL, PostgreSQL
    version = Column(String(20), nullable=False)
    fabricante = Column(String(50))  # Oracle Corporation, MySQL AB
    tipo_gestor = Column(String(50))  # RDBMS, NoSQL, etc.
    fecha_fuera_soporte = Column(Date)
    
    # Relación con instancias
    instancias = relationship(
        "InstanciaBd", 
        back_populates="gestor",
        foreign_keys="[InstanciaBd.gestor_bd_id]"  
    )
    
    def __repr__(self):
        return f"<Gestor(nombre='{self.nombre}', version='{self.version}')>"
    
    def __str__(self):
        return f"{self.nombre} {self.version}"