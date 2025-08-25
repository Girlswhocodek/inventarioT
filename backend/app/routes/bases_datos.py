# app/routes/bases_datos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models.base import get_db
from models.base_datos import BaseDatos
from app.routes.auth import get_current_user

router = APIRouter(tags=["Bases de Datos"])

@router.get("/bases-datos", response_model=List[dict])
async def listar_bases_datos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bases = db.query(BaseDatos).all()
    return [{
        "id": bd.id,
        "nombre": bd.nombre,
        "motor": bd.motor,
        "version": bd.version,
        "fecha_inicio": bd.fecha_inicio,
        "responsable": bd.responsable,
        "espacio_gb": bd.espacio_gb,
        "objetos": bd.objetos,
        "puerto": bd.puerto,
        "estado": bd.estado,
        "sistema_operativo_id": bd.sistema_operativo_id
    } for bd in bases]