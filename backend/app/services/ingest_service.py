from sqlalchemy.orm import Session
from app.models.base import Base
from app.models.base_datos import BaseDatos
from app.models.objeto_bd import ObjetoBD
from app.models.configuration_item import ConfigurationItem
from app.models.kpi_data import KpiData

class IngestService:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------
    # GUARDAR BASES DE DATOS
    # ---------------------------
    def save_database(self, name: str, gestor: str):
        existing = self.db.query(BaseDatos).filter_by(nombre=name).first()

        if existing:
            return existing

        nuevo = BaseDatos(nombre=name, gestor=gestor)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    # ---------------------------
    # GUARDAR TABLAS
    # ---------------------------
    def save_table(self, database_id: int, table_name: str):
        tabla = ObjetoBD(
            base_datos_id=database_id,
            nombre=table_name,
            tipo="table"
        )
        self.db.add(tabla)
        self.db.commit()
        self.db.refresh(tabla)
        return tabla

    # ---------------------------
    # GUARDAR COLUMNAS (Configuration Items)
    # ---------------------------
    def save_column(self, table_id: int, col_data: dict):
        item = ConfigurationItem(
            objeto_bd_id=table_id,
            nombre=col_data["name"],
            tipo=col_data["type"],
            original_type=col_data["original_type"]
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
