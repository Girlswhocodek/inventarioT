# app/routes/gestores.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.base import get_db
from app.models.gestor import Gestor
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Gestores"])

@router.get("/gestores", response_model=List[dict])
async def listar_gestores(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    gestores = db.query(Gestor).all()
    return [{
        "id": g.id,
        "nombre": g.nombre,
        "tipo": g.tipo,
        "version": g.version,
        "permisos_asignados": json.loads(g.permisos_asignados) if g.permisos_asignados else {},
        "configuracion": json.loads(g.configuracion) if g.configuracion else {},
        "url_acceso": g.url_acceso,
        "estado": g.estado,
        "base_datos_id": g.base_datos_id
    } for g in gestores]