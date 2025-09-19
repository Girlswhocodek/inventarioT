from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

usuarios_roles = Table(
    "usuarios_roles",
    Base.metadata,
    Column("usuario_bd_id", Integer, ForeignKey("usuarios_bd.id"), primary_key=True),
    Column("rol_bd_id", Integer, ForeignKey("roles_bd.id"), primary_key=True)
)