from datetime import datetime
from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.ingreso import Ingreso

ingreso_router = APIRouter()

ingresos = []

@ingreso_router.get('/api/v1/ingresos', tags=['ingresos'], response_model=List[Ingreso], description="Returns all ingresos stored")
def get_all_ingresos() -> List[Ingreso]:
    result = []
    for element in ingresos:
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@ingreso_router.get('/api/v1/ingresos/{id}', tags=['ingresos'], response_model=Ingreso, description="Returns data of one specific ingreso")
def get_ingreso(id: int) -> Ingreso:
    for element in ingresos:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@ingreso_router.post('/api/v1/ingresos', tags=['ingresos'], response_model=dict, description="Creates a new ingreso")
def create_ingreso(ingreso: Ingreso = Body()) -> dict:
    global contador
    ingreso.id = contador
    ingreso.fecha = str(datetime.now())
    contador += 1
    ingresos.append(ingreso.model_dump())
    return JSONResponse(content={
        "message": "The ingreso was created successfully",
        "data": ingreso.model_dump()
    }, status_code=201)

@ingreso_router.delete('/api/v1/ingresos/{id}', tags=['ingresos'], response_model=dict, description="Removes specific ingreso")
def remove_user(id: int) -> dict:
    for element in ingresos:
        if element['id'] == id:
            ingresos.remove(element)
            return JSONResponse(content={
                "message": "The ingreso was removed successfully",
                "data": None
            }, status_code=204)
    return JSONResponse(content={
        "message": "The ingreso does not exists",
        "data": None
    }, status_code=404)
    