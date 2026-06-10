# Backward compatibility re-exports
# These are now at app/routers/ and app/views/
from app.routers import (
    auth_router,
    recicladores_router,
    categorias_router,
    usuarios_router,
    premios_router,
    cupones_router,
)
from app.views import (
    public_views_router,
    auth_views_router,
    admin_views_router,
    reciclador_views_router,
    colaborador_views_router,
)

# Legacy names (kept for compatibility)
pages_router = public_views_router
reciclador_router = recicladores_router
categoria_router = categorias_router
