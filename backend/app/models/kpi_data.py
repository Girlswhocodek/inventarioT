import datetime
import enum
from sqlalchemy import Column, Integer, String, Date, BigInteger, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import Base

# Definición del ENUM de estado
class KpiEstado(str, enum.Enum):
    """
    Define los posibles estados de un registro KPI.
    Equivalente a ENUM('completo', 'faltante-bd', 'faltante-cg') en MySQL.
    """
    COMPLETO = "completo"
    FALTANTE_BD = "faltante-bd"
    FALTANTE_CG = "faltante-cg"

class KpiRegistro(Base):
    """
    Modelo de SQLAlchemy para la tabla_kpis que almacena los registros de calidad de datos.
    """
    __tablename__ = "tabla_kpis"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, index=True)
    trafico = Column(String(50), nullable=True) # Puede ser NULL según los datos de prueba
    esquema = Column(String(100), nullable=False, index=True)
    tablas = Column(Integer)
    tipo = Column(String(50))
    
    # Uso de SQLEnum con una clase Enum de Python
    estado = Column(SQLEnum(KpiEstado), nullable=False, index=True)
    
    # Diferencias
    diferencia = Column(Integer)
    diferencia_registros = Column(BigInteger)

    # Conteo de archivos/registros en Origen (CG)
    cant_archivos_cg = Column(Integer)
    cnt_regis_cg = Column(BigInteger) # Usamos cnt_regis_cg para reflejar el campo original
    
    # Conteo de archivos/registros en Destino (DB)
    cant_archivos_db = Column(Integer)
    cant_regis_db = Column(BigInteger)

    fecha_reproceso = Column(Date, nullable=True)
    
    # Timestamps (manejo de default/onupdate en Python para compatibilidad con SQLite)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<KpiRegistro(id={self.id}, fecha={self.fecha}, esquema='{self.esquema}', estado='{self.estado}')>"