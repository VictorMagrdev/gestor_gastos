from datetime import datetime
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.ingreso import Ingreso

from src.config.database import SessionLocal
from src.models.Ingreso import Ingreso as IngresoModel
from fastapi.encoders import jsonable_encoder

ingreso_router = APIRouter()


@ingreso_router.get(
    "/",
    tags=["ingresos"],
    response_model=List[Ingreso],
    description="Returns all ingresos stored",
)
def get_all_ingresos() -> List[Ingreso]:
    db = SessionLocal()
    query = db.query(IngresoModel)
    result = query.all()
    return JSONResponse(content=jsonable_encoder(result),
                        status_code=status.HTTP_200_OK)


@ingreso_router.get(
    "/{id}",
    tags=["ingresos"],
    response_model=Ingreso,
    description="Returns data of one specific ingreso",
)
def get_ingreso(id: int) -> Ingreso:
    db = SessionLocal()
    element = db.query(IngresoModel).filter(IngresoModel.id == id).first()

    if not element:
        return JSONResponse(content={
            "message": "The requested product was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
                        status_code=status.HTTP_200_OK)


@ingreso_router.post(
    "/", tags=["ingresos"],
    response_model=dict,
    description="Creates a new ingreso"
)
def create_ingreso(ingreso: Ingreso = Body()) -> dict:
    db = SessionLocal()
    new_product = IngresoModel(**ingreso.model_dump())
    db.add(new_product)

    db.commit()
    return JSONResponse(content={
        "message": "The product was successfully created",
        "data": ingreso.model_dump()
    }, status_code=status.HTTP_201_CREATED)


@ingreso_router.delete(
    "/{id}",
    tags=["ingresos"],
    response_model=dict,
    description="Removes specific ingreso",
)
def remove_user(id: int) -> dict:
    for element in ingresos:
        if element["id"] == id:
            ingresos.remove(element)
            return JSONResponse(
                content={
                    "message": "The ingreso was removed successfully",
                    "data": None,
                },
                status_code=204,
            )
    return JSONResponse(
        content={"message": "The ingreso does not exists", "data": None},
        status_code=404,
    )
