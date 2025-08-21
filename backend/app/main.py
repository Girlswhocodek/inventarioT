from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi.middleware.cors import CORSMiddleware

# Importar todos los modelos

from models import Base, engine, get_db
from models.servidor import Servidor
from models.sistema_operativo import SistemaOperativo
from models.base_datos import BaseDatos
from models.gestor import Gestor
from models.user import User, pwd_context

# Configuración JWT - CLAVE SECRETA FUNCIONAL
SECRET_KEY = "inventarioT_super_secret_key_2024_prototype_$%&/"  # Clave segura para desarrollo
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="InventarioT API",
    description="Sistema de inventario por 4 niveles: Servidores → SO → BD → Gestores",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funciones de autenticación
def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Crear tablas al iniciar (incluyendo usuarios)
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    crear_datos_prueba()
    crear_usuario_admin()

def crear_usuario_admin():
    from models.base import SessionLocal
    
    db = SessionLocal()
    try:
        # Crear usuario admin por defecto si no existe
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
            print("Usuario admin creado: admin/admin123")
            
        # Crear usuario demo
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
            print("Usuario demo creado: demo/demo123")
    except Exception as e:
        print(f"Error creando usuarios: {e}")
        db.rollback()
    finally:
        db.close()

# Mantén tu función crear_datos_prueba() igual...
def crear_datos_prueba():
    from models.base import SessionLocal
    
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

# Endpoints de autenticación
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
def register_user(username: str, password: str, email: str, full_name: str, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="El usuario o email ya existe")
    
    # Crear nuevo usuario
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username, 
        hashed_password=hashed_password, 
        email=email, 
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuario creado exitosamente"}


@app.get("/dashboard")
async def dashboard():
    """Sirve el dashboard principal"""
    return FileResponse("../frontend/index.html")

@app.get("/", include_in_schema=False)  # include_in_schema=False para ocultar de docs
async def root():
    """Redirige al dashboard desde la raíz"""
    return FileResponse("../frontend/index.html")

# Endpoint público para verificar estado
@app.get("/")
async def root():
    return {
        "message": "InventarioT API funcionando",
        "autenticacion_requerida": True,
        "usuarios_disponibles": [
            {"username": "admin", "password": "admin123"},
            {"username": "demo", "password": "demo123"}
        ],
        "niveles": {
            "1": "Servidores",
            "2": "Sistemas Operativos", 
            "3": "Bases de Datos",
            "4": "Gestores"
        },
        "endpoints": {
            "login": "/token (POST con username, password)",
            "dashboard": "/dashboard",
            "buscar": "/buscar?q=texto&nivel=opcional",
            "servidores": "/servidores",
            "sistemas_operativos": "/sistemas-operativos", 
            "bases_datos": "/bases-datos",
            "gestores": "/gestores",
            "kpis": "/kpis"
        }
    }

# ========== ENDPOINTS PROTEGIDOS ==========

@app.get("/servidores", response_model=List[dict])
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

@app.get("/sistemas-operativos", response_model=List[dict])
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

@app.get("/bases-datos", response_model=List[dict])
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

@app.get("/gestores", response_model=List[dict])
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

# ========== BÚSQUEDA ==========

@app.get("/buscar")
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

# ========== KPIs ==========

@app.get("/kpis")
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

# ========== HEALTH CHECK (público) ==========

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {
            "status": "healthy", 
            "database": "inventario.db",
            "tablas_creadas": True,
            "niveles": 4,
            "autenticacion": "JWT activa"
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

# Servir login
@app.get("/login")
async def login():
    return FileResponse("../frontend/login.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)