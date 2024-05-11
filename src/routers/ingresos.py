from fastapi import APIRouter, Body, status, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from src.config.database import SessionLocal
from src.models.ingreso import Ingreso as IngresoModel
from src.repositories.ingreso import IngresoRepository
from fastapi.encoders import jsonable_encoder

ingreso_router = APIRouter()


@ingreso_router.get(
    "/",
    tags=["ingresos"],
    response_model=List[IngresoModel],
    description="Returns all ingresos stored",
)
def get_all_ingresos(
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
) -> List[IngresoModel]:
    db = SessionLocal()
    result = IngresoRepository(db).get_ingresos(min_valor, max_valor, offset, limit)
    return JSONResponse(
        content=jsonable_encoder(result), status_code=status.HTTP_200_OK
    )


@ingreso_router.get(
    "/{id}",
    tags=["ingresos"],
    response_model=IngresoModel,
    description="Returns data of one specific ingreso",
)
def get_ingreso(id: int = Path(ge=1, le=5000)) -> IngresoModel:
    db = SessionLocal()
    element = IngresoRepository(db).get_ingreso(id)
    if not element:
        return JSONResponse(
            content={"message": "The requested ingreso was not found", "data": None},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        content=jsonable_encoder(element), status_code=status.HTTP_200_OK
    )


@ingreso_router.post(
    "/", tags=["ingresos"], response_model=dict, description="Creates a new ingreso"
)
def create_ingreso(ingreso: IngresoModel = Body()) -> dict:
    db = SessionLocal()
    new_ingreso = IngresoRepository(db).create_ingreso(ingreso)
    return JSONResponse(
        content={
            "message": "The ingreso was successfully created",
            "data": jsonable_encoder(new_ingreso),
        },
        status_code=status.HTTP_201_CREATED,
    )


@ingreso_router.put(
    "/{id}",
    tags=["ingresos"],
    response_model=dict,
    description="Updates the data of specific ingreso",
)
def update_ingreso(id: int = Path(ge=1), ingreso: IngresoModel = Body()) -> dict:
    db = SessionLocal()
    element = IngresoRepository(db).update_ingreso(id, ingreso)
    return JSONResponse(
        content={
            "message": "The ingreso was successfully updated",
            "data": jsonable_encoder(element),
        },
        status_code=status.HTTP_200_OK,
    )


@ingreso_router.delete(
    "/{id}",
    tags=["ingresos"],
    response_model=dict,
    description="Removes specific ingreso",
)
def remove_ingreso(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    IngresoRepository(db).delete_ingreso(id)
    return JSONResponse(
        content={"message": "The ingreso was removed successfully", "data": None},
        status_code=status.HTTP_200_OK,
    )
