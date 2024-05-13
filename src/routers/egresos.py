from fastapi import APIRouter, Body, status, Query, Path
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from src.auth.has_access import security
from fastapi.responses import JSONResponse
from typing import List
from src.config.database import SessionLocal
from src.schemas.egreso import Egreso
from src.repositories.egreso import EgresoRepository
from fastapi.encoders import jsonable_encoder
from src.auth import auth_handler

egreso_router = APIRouter()


@egreso_router.get(
    "/",
    tags=["egresos"],
    response_model=List[Egreso],
    description="Returns all egresos stored",
)
def get_all_egresos(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
) -> List[Egreso]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        result = EgresoRepository(db).get_egresos(min_valor, max_valor, offset, limit)
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@egreso_router.get(
    "/{id}",
    tags=["egresos"],
    response_model=Egreso,
    description="Returns data of one specific egreso",
)
def get_egreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1, le=5000),
) -> Egreso:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        element = EgresoRepository(db).get_egreso(id)
        if not element:
            return JSONResponse(
                content={"message": "The requested egreso was not found", "data": None},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(
            content=jsonable_encoder(element), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@egreso_router.post(
    "/", tags=["egresos"], response_model=dict, description="Creates a new egreso"
)
def create_egreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    egreso: Egreso = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        new_egreso = EgresoRepository(db).create_egreso(egreso)
        return JSONResponse(
            content={
                "message": "The egreso was successfully created",
                "data": jsonable_encoder(new_egreso),
            },
            status_code=status.HTTP_201_CREATED,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@egreso_router.put(
    "/{id}",
    tags=["egresos"],
    response_model=dict,
    description="Updates the data of specific egreso",
)
def update_egreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
    egreso: Egreso = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        element = EgresoRepository(db).update_egreso(id, egreso)
        return JSONResponse(
            content={
                "message": "The egreso was successfully updated",
                "data": jsonable_encoder(element),
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@egreso_router.delete(
    "/{id}",
    tags=["egresos"],
    response_model=dict,
    description="Removes specific egreso",
)
def remove_egreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        EgresoRepository(db).delete_egreso(id)
        return JSONResponse(
            content={"message": "The egreso was removed successfully", "data": None},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
