# app/routes/sistemas_operativos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from app.db.base import get_db
from app.models.sistema_operativo import SistemaOperativo
from app.routes.auth import get_current_user

router = APIRouter(tags=["Sistemas Operativos"])

@router.get("/sistemas-operativos", response_model=List[dict])
async def listar_sistemas_operativos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sistemas = db.query(SistemaOperativo).all()
    return [{
        "id": so.id,
        "nombre": so.nombre,
        "distribucion": so.distribucion,
        "version": so.version,
        "fecha_creacion": so.fecha_creacion,
        "tipo_usuario": so.tipo_usuario,
        "permisos": json.loads(so.permisos) if so.permisos else {},
        "servidor_id": so.servidor_id
    } for so in sistemas]