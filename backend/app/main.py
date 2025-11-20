from datetime import date
from fastapi import FastAPI, Header
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, RedirectResponse
import os
import asyncio
from sqlalchemy import text, inspect
from oracledb import OperationalError

#from app.models.base import Base, engine, get_db
from app.database import Base, SessionLocal, engine, get_db
from app.models.user import User, pwd_context
from app.models.servidor import Servidor
from app.models.sistema_operativo import SistemaOperativo
from app.models.base_datos import BaseDatos
from app.models.gestor import Gestor
from app.models.disco import Disco
from app.models.objeto_bd import ObjetoBd
from app.models.instancia_bd import InstanciaBd
from app.models.empleado import Empleado
from app.models.usuario_bd import UsuarioBd
from app.models.rol_bd import RolBd
from app.models.usuario_rol import usuarios_roles as usuarios_roles_table
from app.routes.extract import router as extract_router


# Importar routers
from app.routes import auth, servidores, sistemas_operativos, bases_datos, gestores, busqueda, kpis




# --- Función para crear usuarios ---
def crear_usuario_admin():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        print("👤 Verificando usuario admin...")
        
        # Verificar si la tabla empleados existe primero
        try:
            db.execute(text("SELECT 1 FROM empleados LIMIT 1"))
        except:
            print("⚠️ Tabla empleado no existe aún, creándola...")
            return False
            
        if db.query(Empleado).filter(Empleado.email == "admin@inventariot.com").first() is None:
            admin_empleado = Empleado(
                nombre_completo="Administrador",
                email="admin@inventariot.com",
                cargo="Administrador de TI",
                usuario="admin"
            )
            db.add(admin_empleado)
            db.commit()
            db.refresh(admin_empleado)
            print("✅ Empleado admin creado")
        else:
            admin_empleado = db.query(Empleado).filter(Empleado.email == "admin@inventariot.com").first()
            print("✅ Empleado admin ya existe")
        
        # Verificar si la tabla users existe
        try:
            db.execute(text("SELECT 1 FROM users LIMIT 1"))
        except:
            print("⚠️ Tabla user no existe aún")
            return False
            
        if db.query(User).filter(User.username == "admin").first() is None:
            hashed_password = pwd_context.hash("admin123")
            admin_user = User(
                username="admin",
                email="admin@inventariot.com",
                hashed_password=hashed_password,
                full_name="Administrador del Sistema",
                is_active=True,
                rol_sistema="admin",
                empleado_id=admin_empleado.id if admin_empleado else None
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
                is_active=True,
                rol_sistema="usuario"
            )
            db.add(demo_user)
            db.commit()
            print("✅ Usuario demo creado: demo/demo123")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        db.rollback()
        return False
    finally:
        db.close()

# --- Función para crear datos de prueba ---
def crear_datos_prueba():
    from datetime import datetime, timedelta
    import json
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        print("📊 Verificando datos de prueba...")
        
        
        try:
            db.execute(text("SELECT 1 FROM servidores LIMIT 1"))
        except:
            print("⚠️ Tabla servidor no existe aún")
            return False
            
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
            
            
            for servidor in servidores:
                db.refresh(servidor)
            
            print(f"✅ {len(servidores)} servidores creados")
            
        try:
            db.execute(text("SELECT 1 FROM bases_datos LIMIT 1"))
        except:
            print("⚠️ Tabla bases_datos no existe aún")
            return False
            
        if db.query(BaseDatos).count() == 0:
            print("📊 Creando datos de prueba...")

            bases_datos = [
        BaseDatos(nombre="ERP_PRODUCCION", motor="Oracle", version="19c",
                  fecha_inicio=datetime.now() - timedelta(days=120),
                  responsable="Ana García", espacio_gb=850.5, objetos=2847,
                  puerto=1521, estado="online",
                  espacio_total_gb=1000.0, espacio_objetos_gb=780.2,
                  permisos_asignados=json.dumps({
                      "usuarios": ["ERP_USER", "ERP_ADMIN", "ERP_READ"],
                      "roles": ["DBA", "CONNECT", "RESOURCE"],
                      "privilegios": ["SELECT", "INSERT", "UPDATE", "DELETE"]
                  }),
                  dblinks=json.dumps(["LINK_TO_WAREHOUSE", "LINK_TO_BACKUP"]),
                  caracter_set="AL32UTF8", nls_characterset="AL16UTF16",
                  fecha_creacion=datetime.now() - timedelta(days=120),
                  instancia_bd_id=1),  
                  
        BaseDatos(nombre="WEB_PORTAL", motor="MySQL", version="8.0.35",
                  fecha_inicio=datetime.now() - timedelta(days=45),
                  responsable="Carlos López", espacio_gb=125.8, objetos=156,
                  puerto=3306, estado="online",
                  espacio_total_gb=200.0, espacio_objetos_gb=98.4,
                  permisos_asignados=json.dumps({
                      "usuarios": ["web_app", "web_admin", "backup_user"],
                      "privilegios": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE"]
                  }),
                  dblinks=json.dumps([]),
                  caracter_set="utf8mb4", nls_characterset="utf8mb4_unicode_ci",
                  fecha_creacion=datetime.now() - timedelta(days=45),
                  instancia_bd_id=1),  
                  
        BaseDatos(nombre="ANALYTICS_DW", motor="PostgreSQL", version="15.4",
                  fecha_inicio=datetime.now() - timedelta(days=60),
                  responsable="María Rodríguez", espacio_gb=2150.7, objetos=489,
                  puerto=5432, estado="online",
                  espacio_total_gb=3000.0, espacio_objetos_gb=1980.3,
                  permisos_asignados=json.dumps({
                      "usuarios": ["analytics_user", "etl_user", "reporting_user"],
                      "roles": ["postgres", "analytics_role"],
                      "privilegios": ["SELECT", "INSERT", "UPDATE", "TRUNCATE"]
                  }),
                  dblinks=json.dumps(["fdw_erp_connection"]),
                  caracter_set="UTF8", nls_characterset="en_US.UTF-8",
                  fecha_creacion=datetime.now() - timedelta(days=60),
                  instancia_bd_id=1),  
                  
        BaseDatos(nombre="CUSTOMERS_API", motor="MongoDB", version="7.0",
                  fecha_inicio=datetime.now() - timedelta(days=30),
                  responsable="Luis Martínez", espacio_gb=45.2, objetos=12,
                  puerto=27017, estado="online",
                  espacio_total_gb=100.0, espacio_objetos_gb=38.7,
                  permisos_asignados=json.dumps({
                      "usuarios": ["api_user", "admin_user"],
                      "roles": ["readWrite", "dbAdmin"],
                      "collections": ["customers", "orders", "products"]
                  }),
                  dblinks=json.dumps([]),
                  caracter_set="UTF-8", nls_characterset="UTF-8",
                  fecha_creacion=datetime.now() - timedelta(days=30),
                  instancia_bd_id=1),  
                  
        BaseDatos(nombre="BACKUP_TESTING", motor="SQL Server", version="2022",
                  fecha_inicio=datetime.now() - timedelta(days=7),
                  responsable="Elena Sánchez", espacio_gb=15.8, objetos=45,
                  puerto=1433, estado="mantenimiento",
                  espacio_total_gb=50.0, espacio_objetos_gb=12.3,
                  permisos_asignados=json.dumps({
                      "usuarios": ["test_user", "backup_admin"],
                      "roles": ["db_datareader", "db_datawriter", "db_owner"],
                      "schemas": ["dbo", "testing"]
                  }),
                  dblinks=json.dumps([]),
                  caracter_set="SQL_Latin1_General_CP1_CI_AS", nls_characterset="Latin1_General_CI_AS",
                  fecha_creacion=datetime.now() - timedelta(days=7),
                  instancia_bd_id=1)  
    ]
            db.add_all(bases_datos)
            db.commit()
            
            for base_dato in bases_datos:
                db.refresh(base_dato)
            
            print(f"✅ {len(bases_datos)} bases creadas")

            try:
                db.execute(text("SELECT 1 FROM sistemas_operativos LIMIT 1"))
                print("✅ Tabla sistema_operativo existe")
                
                
                sistemas = [
                    SistemaOperativo(servidor_id=servidores[0].id, nombre="Windows Server 2022",
                                     distribucion="Windows Server", version="2022",
                                     fecha_creacion=datetime.now() - timedelta(days=29),
                                     tipo_usuario="Administrador",
                                     permisos=json.dumps({"usuarios": ["admin", "backup"], "grupos": ["Administradores"]}),
                                     licencia="Microsoft Volume License"),
                    SistemaOperativo(servidor_id=servidores[1].id, nombre="Ubuntu Server",
                                     distribucion="Linux", version="20.04 LTS",
                                     fecha_creacion=datetime.now() - timedelta(days=14),
                                     tipo_usuario="Root",
                                     permisos=json.dumps({"usuarios": ["root", "www-data"], "grupos": ["sudo"]}),
                                     licencia="GPL")
                ]
                db.add_all(sistemas)
                db.commit()
                
                for sistema in sistemas:
                    db.refresh(sistema)
                
                print(f"✅ {len(sistemas)} sistemas operativos creados")
                
            except Exception as e:
                print(f"⚠️ No se pudieron crear sistemas operativos: {e}")


            
        try:
                db.execute(text("SELECT 1 FROM gestores LIMIT 1"))
                print("✅ Tabla sistema_operativo existe")
        except:
            print("⚠️ Tabla gestores no existe aún")
            return False
        if db.query(Gestor).count() == 0:
            print("📊 Creando datos de prueba...")


            gestores = [
                Gestor(nombre="Oracle Database", version="19c", fabricante="Oracle Corporation",
           tipo_gestor="RDBMS", fecha_fuera_soporte=date(2027, 4, 30)),
                Gestor(nombre="MySQL", version="8.0.35", fabricante="Oracle Corporation",
           tipo_gestor="RDBMS", fecha_fuera_soporte=date(2026, 4, 30)),
                 Gestor(nombre="PostgreSQL", version="15.4", fabricante="PostgreSQL Global Development Group",
           tipo_gestor="RDBMS", fecha_fuera_soporte=date(2027, 11, 11)),
                Gestor(nombre="SQL Server", version="2022", fabricante="Microsoft Corporation",
           tipo_gestor="RDBMS", fecha_fuera_soporte=date(2033, 1, 11)),
                Gestor(nombre="MongoDB", version="7.0", fabricante="MongoDB Inc.",
           tipo_gestor="NoSQL", fecha_fuera_soporte=date(2026, 2, 28))
        ]

            db.add_all(gestores)
            db.commit()
            
            for g in gestores:
                db.refresh(g)
                print(f"✅ {len(gestores)} gestores creados")

            
                print("✅ Datos de prueba creados exitosamente")
            else:
                print("✅ Datos de prueba ya existen")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        db.rollback()
        return False
    finally:
        db.close()

# --- Función para verificar tablas ---
def verificar_tablas():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        print(f"📋 Tablas existentes: {tables}")
        return len(tables) > 0
    except Exception as e:
        print(f"⚠️ Error verificando tablas: {e}")
        return False
    finally:
        db.close()

# --- Lifespan manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Creando todas las tablas...")
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente!")
    
    # Pequeña pausa para asegurar que las tablas están listas
    await asyncio.sleep(1)
    
    # Verificar tablas
    if verificar_tablas():
        print("🔄 Intentando crear usuarios...")
        
        # Intentar crear usuarios (con reintentos)
        max_attempts = 3
        for attempt in range(max_attempts):
            if crear_usuario_admin():
                break
            else:
                print(f"🔄 Reintentando crear usuarios... ({attempt + 1}/{max_attempts})")
                await asyncio.sleep(0.5)
        
        # Pequeña pausa adicional
        await asyncio.sleep(0.5)
        
        print("🔄 Intentando crear datos de prueba...")
        
        # Intentar crear datos de prueba (con reintentos)
        for attempt in range(max_attempts):
            if crear_datos_prueba():
                break
            else:
                print(f"🔄 Reintentando crear datos... ({attempt + 1}/{max_attempts})")
                await asyncio.sleep(0.5)
                
        print("📁 Base de datos inicializada correctamente!")
    else:
        print("❌ No se pudieron verificar las tablas")
    
    yield
    print("🛑 Cerrando conexiones de base de datos...")
# --- Crear app ---
app = FastAPI(
    title="InventarioT API",
    description="Sistema de inventario por 4 niveles: Servidores → SO → BD → Gestores",
    version="1.0.0",
    lifespan=lifespan
)
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


app.mount("/static", StaticFiles(directory="../frontend"), name="static")
app.mount("/css", StaticFiles(directory="../frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")
# --- Routers ---
app.include_router(auth.router, tags=["Authentication"])
app.include_router(servidores.router, tags=["Servidores"])
app.include_router(sistemas_operativos.router, tags=["Sistemas Operativos"])

app.include_router(gestores.router, tags=["Gestores"])
app.include_router(busqueda.router, tags=["Búsqueda"])
app.include_router(kpis.router, tags=["KPIs"])
app.include_router(extract_router)

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

@app.get("/servidores", include_in_schema=False)
async def servidores_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "servidores.html"))

@app.get("/bases-datos", include_in_schema=False)
async def bases_datos_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "bases-datos.html"))

app.include_router(bases_datos.router, prefix="/api", tags=["Bases de Datos"])
@app.get("/sistemas-operativos", include_in_schema=False)
async def sistemas_operativos_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "sistemas-operativos.html"))

# Incluir el router de la API para sistemas operativos
app.include_router(sistemas_operativos.router, prefix="/api", tags=["Sistemas Operativos"])

@app.get("/api/servidores/{servidor_id}/sistemas-operativos")
async def get_sistemas_operativos(servidor_id: int, token: str = Header(...)):
    # Verificar token y devolver SO del servidor
    pass

# --- Health check ---
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok", "message": "API funcionando"}

# --- Ejecutar servidor ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
