# app/routes/kpis.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.base import get_db
from app.models.servidor import Servidor
from app.models.sistema_operativo import SistemaOperativo
from app.models.base_datos import BaseDatos
from app.models.gestor import Gestor
from app.routes.auth import get_current_user

router = APIRouter(tags=["KPIs"])

@router.get("/kpis")
async def obtener_kpis(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_servidores = db.query(Servidor).count()
    servidores_activos = db.query(Servidor).filter(Servidor.estado == "activo").count()
    total_bases_datos = db.query(BaseDatos).count()
    
    return {
        "total_servidores": total_servidores,
        "servidores_activos": servidores_activos,
        "servidores_inactivos": total_servidores - servidores_activos,
        "total_bases_datos": total_bases_datos,
        "total_sistemas_operativos": db.query(SistemaOperativo).count(),
        "total_gestores": db.query(Gestor).count()
    }