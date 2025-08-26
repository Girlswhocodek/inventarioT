
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.models.base import get_db
from app.models.servidor import Servidor
from app.models.sistema_operativo import SistemaOperativo
from app.models.base_datos import BaseDatos
from app.models.gestor import Gestor
from app.models.user import User
from app.routes.auth import get_current_user

router = APIRouter(tags=["Búsqueda"])

@router.get("/buscar")
async def buscar(
    q: str = Query(..., description="Texto a buscar"),
    nivel: Optional[str] = Query(None, description="Filtrar por nivel"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resultados = {}
    
    if not nivel or nivel == "servidores":
        servidores = db.query(Servidor).filter(
            (Servidor.nombre.ilike(f"%{q}%")) |
            (Servidor.ip.ilike(f"%{q}%")) |
            (Servidor.responsable.ilike(f"%{q}%")) |
            (Servidor.estado.ilike(f"%{q}%"))
        ).all()
        resultados["servidores"] = servidores
    
    if not nivel or nivel == "sistemas_operativos":
        sistemas = db.query(SistemaOperativo).filter(
            (SistemaOperativo.nombre.ilike(f"%{q}%")) |
            (SistemaOperativo.distribucion.ilike(f"%{q}%")) |
            (SistemaOperativo.version.ilike(f"%{q}%")) |
            (SistemaOperativo.tipo_usuario.ilike(f"%{q}%"))
        ).all()
        resultados["sistemas_operativos"] = sistemas
    
    if not nivel or nivel == "bases_datos":
        bases = db.query(BaseDatos).filter(
            (BaseDatos.nombre.ilike(f"%{q}%")) |
            (BaseDatos.motor.ilike(f"%{q}%")) |
            (BaseDatos.responsable.ilike(f"%{q}%")) |
            (BaseDatos.estado.ilike(f"%{q}%"))
        ).all()
        resultados["bases_datos"] = bases
    
    if not nivel or nivel == "gestores":
        gestores = db.query(Gestor).filter(
            (Gestor.nombre.ilike(f"%{q}%")) |
            (Gestor.tipo.ilike(f"%{q}%")) |
            (Gestor.version.ilike(f"%{q}%")) |
            (Gestor.estado.ilike(f"%{q}%"))
        ).all()
        resultados["gestores"] = gestores
    
    return resultados