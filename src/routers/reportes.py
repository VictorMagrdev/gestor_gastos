from fastapi import APIRouter, Body, status, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.ingreso import Ingreso
from src.config.database import SessionLocal
from src.models.ingreso import Ingreso as IngresoModel
from src.models.egreso import Egreso as EgresoModel
from fastapi.encoders import jsonable_encoder

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
        "balance": balance
    }

@reportes_router.get('/simple',
                     response_model=dict,
                     description="Reporte con información basica")
def reporte_simple() -> dict:
    db = SessionLocal()
    try:
        query_ingresos = db.query(IngresoModel)
        query_egresos = db.query(EgresoModel)
        ingresos = query_ingresos.all()
        egresos = query_egresos.all()
        return calcular_reporte_simple(ingresos, egresos)
    finally:
        db.close()



@reportes_router.get('/ampliado')
def reporte_ampliado():
    ingresos_agrupados = {}
    egresos_agrupados = {}
    
    db = SessionLocal()
    
    query_ingresos = db.query(IngresoModel)
    query_egresos = db.query(EgresoModel)
    ingresos = query_ingresos.all()
    egresos = query_egresos.all()
    
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
        "reporteS": calcular_reporte_simple(ingresos, egresos)
    }, status_code=200)
