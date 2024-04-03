from typing import List
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, validator
from datetime import datetime
from fastapi.responses import JSONResponse

app = FastAPI()

contador = 0
egresos = []
ingresos = []

ingresos_categorias = ["Pago de nomina", "Pago contrato", "Pago arriendo", "Mesada"]
egreso_categorias= ["alimentacion", "transporte", "ocio", "libros"]
@app.get("/")
def great():
    return {"Hello": "World"}

class Egreso(BaseModel):
    id:                 int | None = Field(default=None, primary_key=True)
    fecha:              str | None = Field(default=None, title="Entry transaction date")
    descripcion:        str = Field(min_length=4, max_length=64, title="entry transaction description")
    valor:              float = Field(default="1000", le=5000000, lg=100, title="Price of entry transaction")
    categoria:          str = Field(min_length=4, max_length=128, title="category of entry transaction")
    
    @validator("categoria")
    @classmethod
    def validar_categoria_egreso(cls, categoria):
        if categoria not in egreso_categorias:
            raise ValueError("Categoria incorrecta para los egresos")
        return categoria
    
class Ingreso(BaseModel):
    id:                 int | None = Field(default=None, primary_key=True)
    fecha:              str | None = Field(default=None, title="Entry transaction date")
    descripcion:        str = Field(min_length=4, max_length=64, title="entry transaction description")
    valor:              float = Field(default="1000", le=5000000, lg=100, title="Price of entry transaction")
    categoria:          str = Field(min_length=4, max_length=128, title="category of entry transaction")

    @validator("categoria")
    @classmethod
    def validar_categoria_ingreso(cls, categoria):
        if categoria not in ingresos_categorias:
            raise ValueError("Categoria incorrecta para los ingresos")
        return categoria
        
#ENDPOINTS INGRESOS
@app.get('/ingresos', tags=['ingresos'], response_model=List[Ingreso], description="Returns all ingresos stored")
def get_all_ingresos() -> List[Ingreso]:
    result = []
    for element in ingresos:
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@app.get('/ingresos/{id}', tags=['ingresos'], response_model=Ingreso, description="Returns data of one specific ingreso")
def get_ingreso(id: int) -> Ingreso:
    for element in ingresos:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@app.post('/ingresos', tags=['ingresos'], response_model=dict, description="Creates a new ingreso")
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

@app.delete('/ingresos/{id}', tags=['ingresos'], response_model=dict, description="Removes specific ingreso")
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
@app.get('/egresos', tags=['egresos'], response_model=List[Egreso], description="Returns all egresos stored")
def get_all_egresos() -> List[Egreso]:
    result = []
    for element in egresos:
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@app.get('/egresos/{id}', tags=['egresos'], response_model=Egreso, description="Returns data of one specific egreso")
def get_egreso(id: int) -> Egreso:
    for element in egresos:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@app.post('/egresos', tags=['egresos'], response_model=dict, description="Creates a new egreso")
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

@app.delete('/egresos/{id}', tags=['egresos'], response_model=dict, description="Removes specific egreso")
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

@app.get('/reporte/simple')
def reporte_simple():
    total_ingresos = 0
    total_egresos = 0

    if len(ingresos) > 0:
        total_ingresos = sum(ingreso.valor for ingreso in ingresos)
    elif len(egresos) > 0 :
        total_egresos = sum(egreso.valor for egreso in egresos)
    
    balance = total_ingresos - total_egresos
    
    return {
        "numero de ingresos": len(ingresos),
        "total_ingresos": total_ingresos,
        "numero de egresos": len(egresos),
        "total_egresos": total_egresos,
        "balance": balance
    }

@app.get('/reporte/ampliado')
def reporte_ampliado():
    ingresos_agrupados = {}
    egresos_agrupados = {}
    for ingreso in ingresos:
        if ingreso.categoria in ingresos_agrupados:
            ingresos_agrupados[ingreso.categoria] += ingreso.valor
        else:
            ingresos_agrupados[ingreso.categoria] = ingreso.valor

    for egreso in egresos:
        if egreso.categoria in egresos_agrupados:
            egresos_agrupados[egreso.categoria] += egreso.valor
        else:
            egresos_agrupados[egreso.categoria] = egreso.valor
    
    return {
        "ingresos_agrupados": ingresos_agrupados,
        "egresos_agrupados": egresos_agrupados
    }
