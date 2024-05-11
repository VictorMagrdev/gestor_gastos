from fastapi import APIRouter, Body, status, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.egreso import Egreso
from src.config.database import SessionLocal
from src.models.egreso import Egreso
from src.repositories.egreso import EgresoRepository
from fastapi.encoders import jsonable_encoder

egreso_router = APIRouter()


@egreso_router.get(
    "/",
    tags=["egresos"],
    response_model=List[Egreso],
    description="Returns all egresos stored",
)
def get_all_egresos(
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
) -> List[Egreso]:
    db = SessionLocal()
    result = EgresoRepository(db).get_egresos(min_valor, max_valor, offset, limit)
    return JSONResponse(
        content=jsonable_encoder(result), status_code=status.HTTP_200_OK
    )


@egreso_router.get(
    "/{id}",
    tags=["egresos"],
    response_model=Egreso,
    description="Returns data of one specific egreso",
)
def get_egreso(id: int = Path(ge=1, le=5000)) -> Egreso:
    db = SessionLocal()
    element = EgresoRepository(db).get_egreso(id)
    if not element:
        return JSONResponse(
            content={"message": "The requested egreso was not found", "data": None},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        content=jsonable_encoder(element), status_code=status.HTTP_200_OK
    )


@egreso_router.post(
    "/", tags=["egresos"], response_model=dict, description="Creates a new egreso"
)
def create_egreso(egreso: Egreso = Body()) -> dict:
    db = SessionLocal()
    new_egreso = EgresoRepository(db).create_egreso(egreso)
    return JSONResponse(
        content={
            "message": "The egreso was successfully created",
            "data": jsonable_encoder(new_egreso),
        },
        status_code=status.HTTP_201_CREATED,
    )


@egreso_router.put(
    "/{id}",
    tags=["egresos"],
    response_model=dict,
    description="Updates the data of specific egreso",
)
def update_egreso(id: int = Path(ge=1), egreso: Egreso = Body()) -> dict:
    db = SessionLocal()
    element = EgresoRepository(db).update_egreso(id, egreso)
    return JSONResponse(
        content={
            "message": "The egreso was successfully updated",
            "data": jsonable_encoder(element),
        },
        status_code=status.HTTP_200_OK,
    )


@egreso_router.delete(
    "/{id}",
    tags=["egresos"],
    response_model=dict,
    description="Removes specific egreso",
)
def remove_egreso(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    EgresoRepository(db).delete_egreso(id)
    return JSONResponse(
        content={"message": "The egreso was removed successfully", "data": None},
        status_code=status.HTTP_200_OK,
    )
