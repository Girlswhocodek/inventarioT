from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, timedelta

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
    crear_datos_prueba()

def crear_datos_prueba():
    from models.base import SessionLocal  # Importación correcta
    
    db = SessionLocal()
    try:
        if db.query(Servidor).count() == 0:
            print("Creando datos de prueba...")
            
            # Crear servidores
            servidores = [
                Servidor(
                    nombre="ERP Server", 
                    ip="192.168.1.200",
                    cpu_nucleos=16,
                    ram_gb=64,
                    almacenamiento_gb=1000,
                    estado="activo",
                    responsable="Ana García",
                    fecha_creacion=datetime.now() - timedelta(days=30)
                ),
                Servidor(
                    nombre="Web Server", 
                    ip="192.168.1.201",
                    cpu_nucleos=8,
                    ram_gb=32,
                    almacenamiento_gb=500,
                    estado="activo", 
                    responsable="Carlos López",
                    fecha_creacion=datetime.now() - timedelta(days=15)
                ),
                Servidor(
                    nombre="DB Server", 
                    ip="192.168.1.202",
                    cpu_nucleos=12,
                    ram_gb=48,
                    almacenamiento_gb=2000,
                    estado="mantenimiento",
                    responsable="María Rodríguez",
                    fecha_creacion=datetime.now() - timedelta(days=10)
                )
            ]
            db.add_all(servidores)
            db.commit()

            # Crear sistemas operativos
            sistemas = [
                SistemaOperativo(
                    servidor_id=1,
                    nombre="Windows Server 2022",
                    distribucion="Windows Server",
                    version="2022",
                    fecha_creacion=datetime.now() - timedelta(days=29),
                    tipo_usuario="Administrador",
                    permisos=json.dumps({"usuarios": ["admin", "backup"], "grupos": ["Administradores"]}),
                    licencia="Microsoft Volume License"
                ),
                SistemaOperativo(
                    servidor_id=2,
                    nombre="Ubuntu Server",
                    distribucion="Linux",
                    version="20.04 LTS",
                    fecha_creacion=datetime.now() - timedelta(days=14),
                    tipo_usuario="Root",
                    permisos=json.dumps({"usuarios": ["root", "www-data"], "grupos": ["sudo"]}),
                    licencia="GPL"
                )
            ]
            db.add_all(sistemas)
            db.commit()

            # Crear bases de datos
            bases_datos = [
                BaseDatos(
                    sistema_operativo_id=1,
                    nombre="ERP_Production",
                    motor="Microsoft SQL Server",
                    version="2019",
                    fecha_inicio=datetime.now() - timedelta(days=28),
                    responsable="Juan Pérez",
                    espacio_gb=250.5,
                    objetos=145,
                    puerto=1433,
                    estado="activo"
                ),
                BaseDatos(
                    sistema_operativo_id=2,
                    nombre="Web_DB",
                    motor="MySQL",
                    version="8.0",
                    fecha_inicio=datetime.now() - timedelta(days=13),
                    responsable="Laura Martínez",
                    espacio_gb=120.3,
                    objetos=89,
                    puerto=3306,
                    estado="activo"
                )
            ]
            db.add_all(bases_datos)
            db.commit()

            # Crear gestores
            gestores = [
                Gestor(
                    base_datos_id=1,
                    nombre="SSMS",
                    tipo="SQL Server Management Studio",
                    version="18.0",
                    permisos_asignados=json.dumps({"lectura": True, "escritura": True, "admin": True}),
                    configuracion=json.dumps({"timeout": 30, "backup_auto": True}),
                    url_acceso="ssms://192.168.1.200",
                    estado="activo"
                ),
                Gestor(
                    base_datos_id=2,
                    nombre="phpMyAdmin",
                    tipo="Web-based Manager",
                    version="5.1",
                    permisos_asignados=json.dumps({"lectura": True, "escritura": True, "admin": False}),
                    configuracion=json.dumps({"theme": "dark", "export_format": "sql"}),
                    url_acceso="http://192.168.1.201/phpmyadmin",
                    estado="activo"
                )
            ]
            db.add_all(gestores)
            db.commit()
            
            print("Datos de prueba creados exitosamente")
            
    except Exception as e:
        print(f"Error creando datos de prueba: {e}")
        db.rollback()
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "InventarioT API funcionando",
        "niveles": {
            "1": "Servidores",
            "2": "Sistemas Operativos", 
            "3": "Bases de Datos",
            "4": "Gestores"
        },
        "endpoints": {
            "dashboard": "/dashboard",
            "buscar": "/buscar?q=texto&nivel=opcional",
            "servidores": "/servidores",
            "sistemas_operativos": "/sistemas-operativos", 
            "bases_datos": "/bases-datos",
            "gestores": "/gestores",
            "kpis": "/kpis"
        }
    }

# ========== ENDPOINTS DE LISTADO ==========

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

# ========== BÚSQUEDA ==========

@app.get("/buscar")
async def buscar(
    q: str = Query(..., description="Texto a buscar"),
    nivel: Optional[str] = Query(None, description="Filtrar por nivel"),
    db: Session = Depends(get_db)
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

# ========== KPIs ==========

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

# ========== HEALTH CHECK ==========

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

# ========== SERVIR FRONTEND ==========

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/dashboard")
async def dashboard():
    return FileResponse("../frontend/index.html")

# Servir el frontend en la raíz también
@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/index.html")
