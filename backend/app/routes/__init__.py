from .auth import router as auth_router
from .servidores import router as servidores_router
from .sistemas_operativos import router as sistemas_operativos_router
from .bases_datos import router as bases_datos_router
from .gestores import router as gestores_router
from .busqueda import router as busqueda_router
from .kpis import router as kpis_router

__all__ = [
    'auth_router',
    'servidores_router', 
    'sistemas_operativos_router',
    'bases_datos_router',
    'gestores_router',
    'busqueda_router',
    'kpis_router'
]