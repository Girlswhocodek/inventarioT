from pydantic import BaseModel


class DatabaseSchema(BaseModel):
    """
    Representa una base de datos dentro del sistema.
    """
    name: str


class TableSchema(BaseModel):
    """
    Representa una tabla perteneciente a una base de datos.
    """
    database: str
    table_name: str


class ColumnSchema(BaseModel):
    """
    Representa una columna dentro de una tabla específica.
    """
    database: str
    table_name: str
    column_name: str
    data_type: str | None = None
    is_nullable: bool | None = None
