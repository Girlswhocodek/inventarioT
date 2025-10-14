from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract
from app.models.base import get_db
# Importa solo el nuevo modelo y la base, los viejos ya no son necesarios
from app.models.kpi_data import KpiRegistro, KpiEstado 
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["KPIs"])

@router.get("/api/kpis/data-quality")
async def obtener_kpis_data_quality(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Calcula y devuelve los KPIs clave de calidad de datos basados en KpiRegistro.
    
    Estos KPIs son útiles para un dashboard de resumen de calidad y completitud.
    """
    
    # --- KPIs de Resumen General ---
    
    total_registros = db.query(KpiRegistro).count()
    
    # Conteo de registros por estado
    conteo_por_estado = db.query(
        KpiRegistro.estado,
        func.count(KpiRegistro.id).label("conteo")
    ).group_by(KpiRegistro.estado).all()
    
    # Inicializar conteos
    conteo_kpis = {
        "total_registros_dia": total_registros,
        "registros_completos": 0,
        "registros_faltantes_bd": 0,
        "registros_faltantes_cg": 0,
        "total_faltantes": 0,
        "porcentaje_completitud": 0.0,
    }

    for estado, conteo in conteo_por_estado:
        if estado == KpiEstado.COMPLETO:
            conteo_kpis["registros_completos"] = conteo
        elif estado == KpiEstado.FALTANTE_BD:
            conteo_kpis["registros_faltantes_bd"] = conteo
        elif estado == KpiEstado.FALTANTE_CG:
            conteo_kpis["registros_faltantes_cg"] = conteo

    conteo_kpis["total_faltantes"] = conteo_kpis["registros_faltantes_bd"] + conteo_kpis["registros_faltantes_cg"]
    
    if total_registros > 0:
        conteo_kpis["porcentaje_completitud"] = round(
            (conteo_kpis["registros_completos"] / total_registros) * 100, 2
        )

    # --- TOP 5 Esquemas por Faltantes ---
    
    top_esquemas = db.query(
        KpiRegistro.esquema,
        func.sum(case(
            (KpiRegistro.estado != KpiEstado.COMPLETO, 1), 
            else_=0
        )).label("conteo_faltantes")
    ).group_by(KpiRegistro.esquema).order_by(func.sum(case(
        (KpiRegistro.estado != KpiEstado.COMPLETO, 1), 
        else_=0
    )).desc()).limit(5).all()


    # --- Tendencia de Faltantes por Mes (similar a la vista SQL) ---
    
    # Nota: SQLite no soporta extract(year_month from ...) pero soporta extract(month from ...)
    # Agruparemos por Mes y Año para simular el DATE_FORMAT('%Y-%m')
    
    tendencia_mensual = db.query(
        extract('year', KpiRegistro.fecha).label("year"),
        extract('month', KpiRegistro.fecha).label("month"),
        func.count().label("total"),
        func.sum(case((KpiRegistro.estado == KpiEstado.COMPLETO, 1), else_=0)).label("completos"),
        func.sum(case((KpiRegistro.estado == KpiEstado.FALTANTE_BD, 1), else_=0)).label("faltantes_bd"),
        func.sum(case((KpiRegistro.estado == KpiEstado.FALTANTE_CG, 1), else_=0)).label("faltantes_cg"),
    ).group_by("year", "month").order_by("year", "month").all()
    
    tendencia_formateada = [
        {
            "mes_anho": f"{row.year:04d}-{row.month:02d}", # Formato YYYY-MM
            "total": row.total,
            "completos": row.completos,
            "faltantes_bd": row.faltantes_bd,
            "faltantes_cg": row.faltantes_cg,
            "porcentaje_completitud": round((row.completos / row.total) * 100, 2) if row.total > 0 else 0.0
        }
        for row in tendencia_mensual
    ]
    
    return {
        "summary_kpis": conteo_kpis,
        "top_5_esquemas_faltantes": [{"esquema": e, "faltantes": c} for e, c in top_esquemas],
        "tendencia_mensual": tendencia_formateada
    }
