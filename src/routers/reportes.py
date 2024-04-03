from datetime import datetime
from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.ingreso import Ingreso
from ingresos import ingresos
from src.schemas.egreso import Egreso
from egresos import egresos

reportes_router = APIRouter()

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

@reportes_router.get('/api/v1/reporte/simple', response_model=dict, description="Reporte con información basica")
def reporte_simple() -> dict:
    return JSONResponse(content=calcular_reporte_simple(), status_code=200)

@reportes_router.get('/api/v1/reporte/ampliado')
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