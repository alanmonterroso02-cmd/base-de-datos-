from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.cupones_repository import CuponRepository
from app.models.reciclador import Reciclador
from app.models.premio import Premio
from app.utils.auth import require_colaborador

router = APIRouter(prefix="/cupones", tags=["Cupones"])


@router.post("/usar")
def usar_cupon(
    codigo: str,
    _: dict = Depends(require_colaborador),
    session: Session = Depends(get_session),
):
    repo = CuponRepository(session)
    cupon = repo.find_by_codigo(codigo)
    if not cupon:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")
    if cupon.esta_usado:
        raise HTTPException(status_code=400, detail="El cupón ya fue usado")

    reciclador = session.get(Reciclador, cupon.reciclador_nit)
    premio = session.get(Premio, cupon.premio_id)

    cupon.esta_usado = True
    session.add(cupon)
    session.commit()

    return {
        "mensaje": "Cupón canjeado exitosamente",
        "codigo": cupon.codigo,
        "reciclador": {
            "nit": reciclador.nit,
            "nombre_completo": reciclador.nombre_completo,
        }
        if reciclador
        else None,
        "premio": {
            "nombre": premio.nombre,
            "imagen": premio.imagen,
            "costo_puntos": float(premio.costo_puntos),
        }
        if premio
        else None,
    }
