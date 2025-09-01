from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os

from app.models.base import Base, engine, get_db
from app.models.user import User, pwd_context
from app.models.servidor import Servidor
from app.models.sistema_operativo import SistemaOperativo
from app.models.base_datos import BaseDatos
from app.models.gestor import Gestor


# Importar routers
from app.routes import auth, servidores, sistemas_operativos, bases_datos, gestores, busqueda, kpis


# --- Función para crear usuarios ---
def crear_usuario_admin():
    db = next(get_db())
    try:
        if db.query(User).filter(User.username == "admin").first() is None:
            hashed_password = pwd_context.hash("admin123")
            admin_user = User(
                username="admin",
                email="admin@inventariot.com",
                hashed_password=hashed_password,
                full_name="Administrador del Sistema",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuario admin creado: admin/admin123")
        if db.query(User).filter(User.username == "demo").first() is None:
            hashed_password = pwd_context.hash("demo123")
            demo_user = User(
                username="demo",
                email="demo@inventariot.com",
                hashed_password=hashed_password,
                full_name="Usuario Demo",
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            print("✅ Usuario demo creado: demo/demo123")
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        db.rollback()
    finally:
        db.close()

# --- Función para crear datos de prueba ---
def crear_datos_prueba():
    from datetime import datetime, timedelta
    import json

    db = next(get_db())
    try:
        if db.query(Servidor).count() == 0:
            print("📊 Creando datos de prueba...")
            # Servidores
            servidores = [
                Servidor(nombre="ERP Server", ip="192.168.1.200", cpu_nucleos=16, ram_gb=64,
                         almacenamiento_gb=1000, estado="activo", responsable="Ana García",
                         fecha_creacion=datetime.now() - timedelta(days=30)),
                Servidor(nombre="Web Server", ip="192.168.1.201", cpu_nucleos=8, ram_gb=32,
                         almacenamiento_gb=500, estado="activo", responsable="Carlos López",
                         fecha_creacion=datetime.now() - timedelta(days=15)),
                Servidor(nombre="DB Server", ip="192.168.1.202", cpu_nucleos=12, ram_gb=48,
                         almacenamiento_gb=2000, estado="mantenimiento", responsable="María Rodríguez",
                         fecha_creacion=datetime.now() - timedelta(days=10))
            ]
            db.add_all(servidores)
            db.commit()
            # Sistemas Operativos
            sistemas = [
                SistemaOperativo(servidor_id=1, nombre="Windows Server 2022",
                                 distribucion="Windows Server", version="2022",
                                 fecha_creacion=datetime.now() - timedelta(days=29),
                                 tipo_usuario="Administrador",
                                 permisos=json.dumps({"usuarios": ["admin", "backup"], "grupos": ["Administradores"]}),
                                 licencia="Microsoft Volume License"),
                SistemaOperativo(servidor_id=2, nombre="Ubuntu Server",
                                 distribucion="Linux", version="20.04 LTS",
                                 fecha_creacion=datetime.now() - timedelta(days=14),
                                 tipo_usuario="Root",
                                 permisos=json.dumps({"usuarios": ["root", "www-data"], "grupos": ["sudo"]}),
                                 licencia="GPL")
            ]
            db.add_all(sistemas)
            db.commit()
            # Bases de Datos
            bases_datos = [
                BaseDatos(sistema_operativo_id=1, nombre="ERP_Production",
                          motor="Microsoft SQL Server", version="2019",
                          fecha_inicio=datetime.now() - timedelta(days=28),
                          responsable="Juan Pérez", espacio_gb=250.5, objetos=145,
                          puerto=1433, estado="activo"),
                BaseDatos(sistema_operativo_id=2, nombre="Web_DB",
                          motor="MySQL", version="8.0",
                          fecha_inicio=datetime.now() - timedelta(days=13),
                          responsable="Laura Martínez", espacio_gb=120.3, objetos=89,
                          puerto=3306, estado="activo")
            ]
            db.add_all(bases_datos)
            db.commit()
            # Gestores
            gestores = [
                Gestor(base_datos_id=1, nombre="SSMS", tipo="SQL Server Management Studio",
                       version="18.0", permisos_asignados=json.dumps({"lectura": True, "escritura": True, "admin": True}),
                       configuracion=json.dumps({"timeout": 30, "backup_auto": True}),
                       url_acceso="ssms://192.168.1.200", estado="activo"),
                Gestor(base_datos_id=2, nombre="phpMyAdmin", tipo="Web-based Manager",
                       version="5.1", permisos_asignados=json.dumps({"lectura": True, "escritura": True, "admin": False}),
                       configuracion=json.dumps({"theme": "dark", "export_format": "sql"}),
                       url_acceso="http://192.168.1.201/phpmyadmin", estado="activo")
            ]
            db.add_all(gestores)
            db.commit()
            print("✅ Datos de prueba creados exitosamente")
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        db.rollback()
    finally:
        db.close()

# --- Lifespan manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Creando todas las tablas...")
    Base.metadata.create_all(bind=engine)
    crear_usuario_admin()
    crear_datos_prueba()
    print("✅ Tablas creadas exitosamente!")
    print("📁 Base de datos creada en: inventario.db")
    yield
    print("🛑 Cerrando conexiones de base de datos...")

# --- Crear app ---
app = FastAPI(
    title="InventarioT API",
    description="Sistema de inventario por 4 niveles: Servidores → SO → BD → Gestores",
    version="1.0.0",
    lifespan=lifespan
)

# --- Configuración CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#servir
app.mount("/static", StaticFiles(directory="../frontend"), name="static")
app.mount("/css", StaticFiles(directory="../frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")
# --- Routers ---
app.include_router(auth.router, tags=["Authentication"])
#app.include_router(servidores.router, tags=["Servidores"])
#app.include_router(sistemas_operativos.router, tags=["Sistemas Operativos"])
#app.include_router(bases_datos.router, tags=["Bases de Datos"])
#app.include_router(gestores.router, tags=["Gestores"])
app.include_router(busqueda.router, tags=["Búsqueda"])
app.include_router(kpis.router, tags=["KPIs"])

# --- Rutas absolutas para archivos estáticos ---
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))


# Montar frontend completo (HTML + CSS + JS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- Endpoints de frontend ---
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/login")

@app.get("/login", include_in_schema=False)
async def login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/kpis", include_in_schema=False)
async def kpis():
    return FileResponse(os.path.join(FRONTEND_DIR, "kpis.html"))

# --- Health check ---
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok", "message": "API funcionando"}

# --- Ejecutar servidor ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
