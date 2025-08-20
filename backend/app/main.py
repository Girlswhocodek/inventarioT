from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

# Importar todos los modelos
from models import Base, engine, get_db
from models.servidor import Servidor
from models.sistema_operativo import SistemaOperativo
from models.base_datos import BaseDatos
from models.gestor import Gestor

app = FastAPI(
    title="InventarioT API",
    description="Sistema de inventario por 4 niveles: Servidores → SO → BD → Gestores",
    version="1.0.0"
)

# Crear tablas al iniciar
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {
        "message": "✅ InventarioT API funcionando",
        "niveles": {
            "1": "Servidores",
            "2": "Sistemas Operativos", 
            "3": "Bases de Datos",
            "4": "Gestores"
        },
        "endpoints": {
            "servidores": "/servidores",
            "sistemas_operativos": "/sistemas-operativos", 
            "bases_datos": "/bases-datos",
            "gestores": "/gestores"
        }
    }

# ========== NIVEL 1: SERVIDORES ==========
@app.get("/servidores", response_model=List[dict])
async def listar_servidores(db: Session = Depends(get_db)):
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

# ========== NIVEL 2: SISTEMAS OPERATIVOS ==========
@app.get("/sistemas-operativos", response_model=List[dict])
async def listar_sistemas_operativos(db: Session = Depends(get_db)):
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

# ========== NIVEL 3: BASES DE DATOS ==========
@app.get("/bases-datos", response_model=List[dict])
async def listar_bases_datos(db: Session = Depends(get_db)):
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

# ========== NIVEL 4: GESTORES ==========
@app.get("/gestores", response_model=List[dict])
async def listar_gestores(db: Session = Depends(get_db)):
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

# Health check
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {
            "status": "healthy", 
            "database": "inventario.db",
            "tablas_creadas": True,
            "niveles": 4
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# KPIs para dashboard
@app.get("/kpis")
async def obtener_kpis(db: Session = Depends(get_db)):
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
