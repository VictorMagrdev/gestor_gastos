from typing import List
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, validator
from datetime import datetime
from fastapi.responses import JSONResponse
from src.middlewares.error_handler import ErrorHandler
from src.schemas.ingreso import Ingreso
from src.schemas.egreso import Egreso

app = FastAPI()

app.add_middleware(ErrorHandler)

contador = 0
egresos = []
ingresos = []

@app.get("/api/v1")
def great():
    return {"Hello": "World"}
        
#ENDPOINTS INGRESOS
@app.get('/api/v1/ingresos', tags=['ingresos'], response_model=List[Ingreso], description="Returns all ingresos stored")
def get_all_ingresos() -> List[Ingreso]:
    result = []
    for element in ingresos:
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@app.get('/api/v1/ingresos/{id}', tags=['ingresos'], response_model=Ingreso, description="Returns data of one specific ingreso")
def get_ingreso(id: int) -> Ingreso:
    for element in ingresos:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@app.post('/api/v1/ingresos', tags=['ingresos'], response_model=dict, description="Creates a new ingreso")
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

@app.delete('/api/v1/ingresos/{id}', tags=['ingresos'], response_model=dict, description="Removes specific ingreso")
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
    
#egresos
@app.get('/api/v1/egresos', tags=['egresos'], response_model=List[Egreso], description="Returns all egresos stored")
def get_all_egresos() -> List[Egreso]:
    result = []
    for element in egresos:
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@app.get('/api/v1/egresos/{id}', tags=['egresos'], response_model=Egreso, description="Returns data of one specific egreso")
def get_egreso(id: int) -> Egreso:
    for element in egresos:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@app.post('/api/v1/egresos', tags=['egresos'], response_model=dict, description="Creates a new egreso")
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

@app.delete('/api/v1/egresos/{id}', tags=['egresos'], response_model=dict, description="Removes specific egreso")
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

def calcular_reporte_simple():
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
        "balance": balance
    }

@app.get('/api/v1/reporte/simple', response_model=dict, description="Reporte con información basica")
def reporte_simple() -> dict:
    return JSONResponse(content=calcular_reporte_simple(), status_code=200)

@app.get('/api/v1/reporte/ampliado')
def reporte_ampliado():
    ingresos_agrupados = {}
    egresos_agrupados = {}
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

    return JSONResponse(content={
        "ingresos_agrupados": ingresos_agrupados,
        "egresos_agrupados": egresos_agrupados,
        "reporteS": calcular_reporte_simple()
    }, status_code=200)
