from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Disco(Base):
    __tablename__ = "discos"
    
    id = Column(Integer, primary_key=True, index=True)
    unidad = Column(String(10))  # C:, D:, /dev/sda1, /dev/sdb1
    espacio_total_gb = Column(Numeric(10,2))  # Espacio total individual
    espacio_usado_gb = Column(Numeric(10,2))
    espacio_libre_gb = Column(Numeric(10,2))
    tipo = Column(String(20))  # SSD, HDD, NVMe
    filesystem = Column(String(20))  # NTFS, EXT4, XFS
    punto_montaje = Column(String(100))  # /, /home, /var
    
    # Relación
    servidor_id = Column(Integer, ForeignKey('servidores.id'), nullable=False)
    servidor = relationship("Servidor", back_populates="discos")