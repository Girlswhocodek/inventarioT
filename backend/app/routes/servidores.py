# app/routes/servidores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.base import get_db
from app.models.servidor import Servidor
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Servidores"])

@router.get("/servidores", response_model=List[dict])
async def listar_servidores(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    servidores = db.query(Servidor).all()
    return [{
        "id": s.id,
        "nombre": s.nombre,
        "ip": s.ip,
        "cpu_nucleos": s.cpu_nucleos,
        "ram_gb": s.ram_gb,
        "almacenamiento_gb": s.almacenamiento_gb,
        "estado": s.estado,
        "responsable": s.responsable,
        "fecha_creacion": s.fecha_creacion
    } for s in servidores]