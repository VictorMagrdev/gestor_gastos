from datetime import datetime
from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.egreso import Egreso

egresos_router = APIRouter()

egresos = []

#egresos
@egresos_router.get('/api/v1/egresos', tags=['egresos'], response_model=List[Egreso], description="Returns all egresos stored")
def get_all_egresos() -> List[Egreso]:
    result = []
    for element in egresos:
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@egresos_router.get('/api/v1/egresos/{id}', tags=['egresos'], response_model=Egreso, description="Returns data of one specific egreso")
def get_egreso(id: int) -> Egreso:
    for element in egresos:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@egresos_router.post('/api/v1/egresos', tags=['egresos'], response_model=dict, description="Creates a new egreso")
def create_egreso(egreso: Egreso = Body()) -> dict:
    global contador
    egreso.id = contador
    egreso.fecha = str(datetime.now())
    contador += 1
    egresos.append(egreso.model_dump())
    return JSONResponse(content={
        "message": "The user was created successfully",
        "data": egreso.model_dump()
    }, status_code=201)

@egresos_router.delete('/api/v1/egresos/{id}', tags=['egresos'], response_model=dict, description="Removes specific egreso")
def remove_egreso(id: int) -> dict:
    for element in egresos:
        if element['id'] == id:
            egresos.remove(element)
            return JSONResponse(content={
                "message": "The egreso was removed successfully",
                "data": None
            }, status_code=204)
    return JSONResponse(content={
        "message": "The egreso does not exists",
        "data": None
    }, status_code=404)
