from fastapi import APIRouter, Body,  status, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.egreso import Egreso
from src.config.database import SessionLocal
from src.models.egreso import Egreso as EgresoModel
from fastapi.encoders import jsonable_encoder

egresos_router = APIRouter()


@egresos_router.get('/',
                    tags=['egresos'],
                    response_model=List[Egreso],
                    description="Returns all egresos stored")
def get_all_ingresos(offset: int = Query(default=None, min=0),
                    limit: int = Query(default=None, min=1)) -> List[Egreso]:
    db = SessionLocal()
    query = db.query(EgresoModel)
    result = query.all()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@egresos_router.get('/{id}',
                    tags=['egresos'],
                    response_model=Egreso,
                    description="Returns data of one specific ingreso")
def get_ingreso(id: int = Path(ge=1, le=5000)) -> Egreso:
    db = SessionLocal()
    element = db.query(EgresoModel).filter(EgresoModel.id == id).first()
    
    if not element:
        return JSONResponse(content={
            "message": "The requested ingreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    return JSONResponse(content=jsonable_encoder(element),
                        status_code=status.HTTP_200_OK)


@egresos_router.post('/',
                     tags=['egresos'],
                     response_model=dict,
                     description="Creates a new egreso")
def create_ingreso(ingreso: Egreso = Body()) -> dict:
    db = SessionLocal()
    new_egreso = EgresoModel(**ingreso.model_dump())
    db.add(new_egreso)
    db.commit()
    
    return JSONResponse(content={
        "message": "The ingreso was successfully created",
        "data": ingreso.model_dump()
    }, status_code=status.HTTP_201_CREATED)


@egresos_router.put('/{id}',
                    tags=['egresos'],
                    response_model=dict,
                    description="Updates the data of specific egreso")
def update_ingreso(id: int = Path(ge=1),
    ingreso: Egreso = Body()) -> dict:
    db = SessionLocal()
    
    element = db.query(EgresoModel).filter(EgresoModel.id == id).first()
    if not element:
        return JSONResponse(content={
            "message": "The requested Egreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    element.descripcion = ingreso.descripcion
    element.valor = ingreso.valor
    element.categoria = ingreso.categoria
    db.commit()
    
    return JSONResponse(content={
        "message": "The Egreso was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)


@egresos_router.delete('/{id}',
                       tags=['egresos'],
                       response_model=dict,
                       description="Removes specific egreso")
def remove_product(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = db.query(EgresoModel).filter(EgresoModel.id == id).first()
    if not element:
        return JSONResponse(content={
        "message": "The requested egreso was not found",
        "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    db.delete(element)
    db.commit()
    return JSONResponse(content={
        "message": "The egreso wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
    