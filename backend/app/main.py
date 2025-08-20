from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importaciones propias
from models.base import Base, engine, get_db
from models.configuration_item import ConfigurationItemDB
from schemas.configuration_item import ConfigurationItem, ConfigurationItemCreate
from crud.configuration_item import get_configuration_items, get_configuration_item, create_configuration_item

app = FastAPI(
    title="CMDB Inventory API - SQLAlchemy + PostgreSQL",
    description="Sistema profesional con ORM y base de datos real",
    version="1.0.0"
)

# Crear tablas al iniciar
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {
        "message": "✅ CMDB con SQLAlchemy + PostgreSQL funcionando!",
        "orm": "SQLAlchemy 2.0",
        "database": "PostgreSQL"
    }

@app.get("/items", response_model=List[ConfigurationItem])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_configuration_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=ConfigurationItem)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_configuration_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items", response_model=ConfigurationItem)
async def create_item(item: ConfigurationItemCreate, db: Session = Depends(get_db)):
    return create_configuration_item(db=db, item=item)

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "orm": "sqlalchemy"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
