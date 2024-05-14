from fastapi import APIRouter, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.config.database import SessionLocal
from src.repositories.egreso import EgresoRepository
from src.repositories.ingreso import IngresoRepository
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from src.auth.has_access import security
from src.auth import auth_handler

reportes_router = APIRouter()


def calcular_reporte_simple(ingresos, egresos):
    total_ingresos = 0
    total_egresos = 0

    if len(ingresos) > 0:
        for ingreso in ingresos:
            total_ingresos += ingreso["valor"]
    if len(egresos) > 0:
        for egreso in egresos:
            total_egresos += egreso["valor"]

    balance = total_ingresos - total_egresos

    return {
        "numero de ingresos": len(ingresos),
        "total_ingresos": total_ingresos,
        "numero de egresos": len(egresos),
        "total_egresos": total_egresos,
        "balance": balance,
    }


@reportes_router.get(
    "/simple", response_model=dict, description="Reporte con información basica"
)
def reporte_simple(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        ingresos = IngresoRepository(db).get_ingresos(
            min_valor, max_valor, offset, limit, owner_id
        )
        ingresos = jsonable_encoder(ingresos)
        egresos = EgresoRepository(db).get_egresos(
            min_valor, max_valor, offset, limit, owner_id
        )
        egresos = jsonable_encoder(egresos)
        return calcular_reporte_simple(ingresos, egresos)
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@reportes_router.get("/ampliado")
def reporte_ampliado(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
):
    if auth_handler.verify_jwt(credentials):
        ingresos_agrupados = {}
        egresos_agrupados = {}

        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        ingresos = IngresoRepository(db).get_ingresos(
            min_valor, max_valor, offset, limit, owner_id
        )
        ingresos = jsonable_encoder(ingresos)
        egresos = EgresoRepository(db).get_egresos(
            min_valor, max_valor, offset, limit, owner_id
        )
        egresos = jsonable_encoder(egresos)

        for ingreso in ingresos:
            if ingreso["categoria"] in ingresos_agrupados:
                ingresos_agrupados[ingreso["categoria"]] += ingreso["valor"]
            else:
                ingresos_agrupados[ingreso["categoria"]] = ingreso["valor"]

        for egreso in egresos:
            if egreso["categoria"] in egresos_agrupados:
                egresos_agrupados[egreso["categoria"]] += egreso["valor"]
            else:
                egresos_agrupados[egreso["categoria"]] = egreso["valor"]

        return JSONResponse(
            content={
                "ingresos_agrupados": ingresos_agrupados,
                "egresos_agrupados": egresos_agrupados,
                "reporteS": calcular_reporte_simple(ingresos, egresos),
            },
            status_code=200,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
