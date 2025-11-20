from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.extractors.extractor_factory import get_extractor

router = APIRouter(prefix="/extract", tags=["Extract"])


# --------------------------
# Schemas para la conexión
# --------------------------
class DBConnection(BaseModel):
    db_type: str         # postgres, mysql, oracle, sqlserver
    host: str
    port: int
    user: str
    password: str
    database: Optional[str] = None   # Python 3.9 compatible
    table: Optional[str] = None      # Solo usado en /columns


# --------------------------
# Crear instancia de extractor
# --------------------------
def get_extractor_instance(conn: DBConnection):
    try:
        extractor = get_extractor(
            db_type=conn.db_type.lower(),
            host=conn.host,
            port=conn.port,
            user=conn.user,
            password=conn.password,
            database=conn.database,
        )
        extractor.connect()
        return extractor

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------------
# 1. Obtener lista de databases
# --------------------------
@router.post("/databases")
def extract_databases(conn: DBConnection):
    extractor = get_extractor_instance(conn)
    try:
        result = extractor.extract_databases()
        return {"databases": result}
    finally:
        extractor.close()


# --------------------------
# 2. Obtener tablas
# --------------------------
@router.post("/tables")
def extract_tables(conn: DBConnection):
    extractor = get_extractor_instance(conn)
    try:
        result = extractor.extract_tables(conn.database)
        return {"tables": result}
    finally:
        extractor.close()


# --------------------------
# 3. Obtener columnas
# --------------------------
@router.post("/columns")
def extract_columns(conn: DBConnection):
    if conn.table is None:
        raise HTTPException(status_code=400, detail="Debe enviar 'table' en el body.")

    extractor = get_extractor_instance(conn)
    try:
        result = extractor.extract_columns(conn.database, conn.table)
        return {"columns": result}
    finally:
        extractor.close()


# ----------------------------------
# 4. Obtener todo el metadata junto
# ----------------------------------
@router.post("/metadata")
def extract_full_metadata(conn: DBConnection):
    extractor = get_extractor_instance(conn)
    try:
        metadata = {
            "databases": extractor.extract_databases(),
            "tables": extractor.extract_tables(conn.database),
            "columns": extractor.extract_columns(conn.database, conn.table) if conn.table else None
        }
        return metadata
    finally:
        extractor.close()

# -------------------------------------------
# 5. EJECUTAR TODO EL PIPELINE ETL COMPLETO
# -------------------------------------------
@router.post("/load-all")
def load_all_pipeline(conn: DBConnection):
    try:
        from app.services.ingest_service import ingest_all_metadata

        result = ingest_all_metadata(
            db_type=conn.db_type.lower(),
            host=conn.host,
            port=conn.port,
            user=conn.user,
            password=conn.password,
            database=conn.database,
        )

        return {
            "status": "success",
            "message": "ETL ejecutado correctamente.",
            "result": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
