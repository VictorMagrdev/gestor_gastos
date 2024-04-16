from fastapi import APIRouter, Body, status, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.ingreso import Ingreso
from src.config.database import SessionLocal
from src.models.ingreso import Ingreso as IngresoModel
from fastapi.encoders import jsonable_encoder

ingreso_router = APIRouter()

@ingreso_router.get('/',
                    tags=['ingresos'],
                    response_model=List[Ingreso],
                    description="Returns all ingresos stored")
def get_all_ingresos(offset: int = Query(default=None, min=0),
                    limit: int = Query(default=None, min=1)) -> List[Ingreso]:
    db = SessionLocal()
    query = db.query(IngresoModel)
    result = query.all()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

    
@ingreso_router.get('/{id}',
                    tags=['ingresos'],
                    response_model=Ingreso,
                    description="Returns data of one specific ingreso")
def get_ingreso(id: int = Path(ge=1, le=5000)) -> Ingreso:
    db = SessionLocal()
    element = db.query(IngresoModel).filter(IngresoModel.id == id).first()
    
    if not element:
        return JSONResponse(content={
            "message": "The requested ingreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    return JSONResponse(content=jsonable_encoder(element),
                        status_code=status.HTTP_200_OK)


@ingreso_router.post('/',
                     tags=['ingresos'],
                     response_model=dict,
                     description="Creates a new ingreso")
def create_ingreso(ingreso: Ingreso = Body()) -> dict:
    db = SessionLocal()
    new_ingreso = IngresoModel(**ingreso.model_dump())
    db.add(new_ingreso)
    db.commit()
    
    return JSONResponse(content={
        "message": "The ingreso was successfully created",
        "data": ingreso.model_dump()
    }, status_code=status.HTTP_201_CREATED)


@ingreso_router.put('/{id}',
                    tags=['ingresos'],
                    response_model=dict,
                    description="Updates the data of specific ingreso")
def update_ingreso(id: int = Path(ge=1),
    ingreso: Ingreso = Body()) -> dict:
    db = SessionLocal()
    
    element = db.query(IngresoModel).filter(IngresoModel.id == id).first()
    if not element:
        return JSONResponse(content={
            "message": "The requested ingreso was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    element.descripcion = ingreso.descripcion
    element.valor = ingreso.valor
    element.categoria = ingreso.categoria
    db.commit()
    
    return JSONResponse(content={
        "message": "The ingreso was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)


@ingreso_router.delete('/{id}',
                       tags=['ingresos'],
                       response_model=dict,
                       description="Removes specific ingreso")
def remove_product(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = db.query(IngresoModel).filter(IngresoModel.id == id).first()
    if not element:
        return JSONResponse(content={
        "message": "The requested Ingreso was not found",
        "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    db.delete(element)
    db.commit()
    return JSONResponse(content={
        "message": "The Ingreso wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
    