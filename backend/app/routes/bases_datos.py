# app/routes/bases_datos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

# CORREGIR: Importar get_db desde el lugar correcto
from app.database import get_db
from app.models.base_datos import BaseDatos
from app.models.instancia_bd import InstanciaBd
from app.models.empleado import Empleado
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Bases de Datos"])

@router.get("/bases-datos", response_model=List[dict])
async def listar_bases_datos(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Obtener todas las bases de datos con información completa"""
    try:
        bases = db.query(BaseDatos).all()
        result = []
        
        for bd in bases:
            base_data = {
                "id": bd.id,
                "nombre": bd.nombre,
                "motor": bd.motor,
                "version": bd.version,
                "fecha_inicio": bd.fecha_inicio.isoformat() if bd.fecha_inicio else None,
                "responsable": bd.responsable,
                "espacio_gb": float(bd.espacio_gb) if bd.espacio_gb else 0,
                "objetos": bd.objetos,
                "puerto": bd.puerto,
                "estado": bd.estado,
                "fecha_creacion": bd.fecha_creacion.isoformat() if bd.fecha_creacion else None,
                "fecha_actualizacion": bd.fecha_actualizacion.isoformat() if bd.fecha_actualizacion else None,
                "espacio_total_gb": float(bd.espacio_total_gb) if bd.espacio_total_gb else 0,
                "espacio_objetos_gb": float(bd.espacio_objetos_gb) if bd.espacio_objetos_gb else 0,
                "caracter_set": bd.caracter_set,
                "nls_characterset": bd.nls_characterset,
                "instancia_bd_id": bd.instancia_bd_id,
                "administrador_id": bd.administrador_id,
                "porcentaje_uso_espacio": bd.porcentaje_uso_espacio,
                "esta_online": bd.esta_online(),
                "url_conexion": bd.url_conexion
            }
            
            # Procesar campos JSON
            try:
                base_data["permisos_asignados"] = json.loads(bd.permisos_asignados) if bd.permisos_asignados else None
            except:
                base_data["permisos_asignados"] = bd.permisos_asignados
                
            try:
                base_data["dblinks"] = json.loads(bd.dblinks) if bd.dblinks else []
            except:
                base_data["dblinks"] = bd.dblinks
                
            result.append(base_data)
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener bases de datos: {str(e)}")

@router.get("/bases-datos/{bd_id}", response_model=dict)
async def obtener_base_datos(
    bd_id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Obtener una base de datos específica por ID"""
    try:
        bd = db.query(BaseDatos).filter(BaseDatos.id == bd_id).first()
        if not bd:
            raise HTTPException(status_code=404, detail="Base de datos no encontrada")
        
        # Construir respuesta
        base_data = {
            "id": bd.id,
            "nombre": bd.nombre,
            "motor": bd.motor,
            "version": bd.version,
            "fecha_inicio": bd.fecha_inicio.isoformat() if bd.fecha_inicio else None,
            "responsable": bd.responsable,
            "espacio_gb": float(bd.espacio_gb) if bd.espacio_gb else 0,
            "objetos": bd.objetos,
            "puerto": bd.puerto,
            "estado": bd.estado,
            "fecha_creacion": bd.fecha_creacion.isoformat() if bd.fecha_creacion else None,
            "fecha_actualizacion": bd.fecha_actualizacion.isoformat() if bd.fecha_actualizacion else None,
            "espacio_total_gb": float(bd.espacio_total_gb) if bd.espacio_total_gb else 0,
            "espacio_objetos_gb": float(bd.espacio_objetos_gb) if bd.espacio_objetos_gb else 0,
            "caracter_set": bd.caracter_set,
            "nls_characterset": bd.nls_characterset,
            "instancia_bd_id": bd.instancia_bd_id,
            "administrador_id": bd.administrador_id,
            "porcentaje_uso_espacio": bd.porcentaje_uso_espacio,
            "esta_online": bd.esta_online(),
            "url_conexion": bd.url_conexion
        }
        
        # Procesar campos JSON
        try:
            base_data["permisos_asignados"] = json.loads(bd.permisos_asignados) if bd.permisos_asignados else None
        except:
            base_data["permisos_asignados"] = bd.permisos_asignados
            
        try:
            base_data["dblinks"] = json.loads(bd.dblinks) if bd.dblinks else []
        except:
            base_data["dblinks"] = bd.dblinks
        
        # Información de relaciones
        if bd.instancia_bd:
            base_data["instancia_bd"] = {
                "id": bd.instancia_bd.id,
                "nombre": bd.instancia_bd.nombre,
                "version": bd.instancia_bd.version,
                "puerto": bd.instancia_bd.puerto,
                "espacio_asignado_gb": float(bd.instancia_bd.espacio_asignado_gb) if bd.instancia_bd.espacio_asignado_gb else 0,
                "url_conexion": bd.instancia_bd.url_conexion
            }
            
            if bd.instancia_bd.servidor:
                base_data["servidor"] = {
                    "id": bd.instancia_bd.servidor.id,
                    "nombre": bd.instancia_bd.servidor.nombre,
                    "ip": bd.instancia_bd.servidor.ip
                }
        
        if bd.administrador:
            base_data["administrador"] = {
                "id": bd.administrador.id,
                "nombre_completo": bd.administrador.nombre_completo,
                "email": bd.administrador.email,
                "cargo": bd.administrador.cargo
            }
        
        # Información de objetos relacionados
        base_data["objetos_bd"] = [{
            "id": obj.id,
            "nombre": obj.nombre,
            "tipo": obj.tipo,
            "tamaño_mb": float(obj.tamaño_mb) if obj.tamaño_mb else 0
        } for obj in bd.objetos_bd] if bd.objetos_bd else []
        
        base_data["usuarios_bd"] = [{
            "id": usuario.id,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "fecha_creacion": usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else None
        } for usuario in bd.usuarios_bd] if bd.usuarios_bd else []
        
        return base_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la base de datos: {str(e)}")

@router.get("/bases-datos/estadisticas/resumen", response_model=dict)
async def obtener_estadisticas_bases_datos(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Obtener estadísticas resumidas de todas las bases de datos"""
    try:
        total_bases = db.query(BaseDatos).count()
        bases_online = db.query(BaseDatos).filter(BaseDatos.estado == "online").count()
        bases_offline = total_bases - bases_online
        
        # Agrupar por motor
        motores = db.query(BaseDatos.motor, db.func.count(BaseDatos.id)).group_by(BaseDatos.motor).all()
        
        # Espacio total utilizado
        espacio_total = db.query(db.func.sum(BaseDatos.espacio_total_gb)).scalar() or 0
        
        return {
            "total_bases_datos": total_bases,
            "bases_online": bases_online,
            "bases_offline": bases_offline,
            "espacio_total_gb": float(espacio_total),
            "distribucion_motores": {motor: count for motor, count in motores},
            "porcentaje_online": round((bases_online / total_bases * 100), 2) if total_bases > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")