from fastapi import APIRouter, Body, status, Query, Path
from fastapi.responses import JSONResponse
from typing import List
from src.config.database import SessionLocal
from src.schemas.ingreso import Ingreso, IngresoCreate
from src.repositories.ingreso import IngresoRepository
from fastapi.encoders import jsonable_encoder
from src.auth import auth_handler
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from fastapi import Depends

ingreso_router = APIRouter()


@ingreso_router.get(
    "/",
    tags=["ingresos"],
    response_model=List[Ingreso],
    description="Returns all ingresos stored",
)
def get_all_ingresos(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    min_valor: float = Query(default=None, min=10, max=5000000),
    max_valor: float = Query(default=None, min=10, max=5000000),
    offset: int = Query(default=None, min=0),
    limit: int = Query(default=None, min=1),
) -> List[Ingreso]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        result = IngresoRepository(db).get_ingresos(
            min_valor, max_valor, offset, limit, owner_id
        )
        return JSONResponse(
            content=jsonable_encoder(result), status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@ingreso_router.get(
    "/{id}",
    tags=["ingresos"],
    response_model=Ingreso,
    description="Returns data of one specific ingreso",
)
def get_ingreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1, le=5000),
) -> Ingreso:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        element = IngresoRepository(db).get_ingreso(id)
        if not element:
            return JSONResponse(
                content={
                    "message": "The requested ingreso was not found",
                    "data": None,
                },
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


@ingreso_router.post(
    "/", tags=["ingresos"], response_model=dict, description="Creates a new ingreso"
)
def create_ingreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    ingreso: IngresoCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        owner_id = auth_handler.decode_token(credential)["user.id"]
        new_ingreso = IngresoRepository(db).create_ingreso(ingreso, owner_id)
        return JSONResponse(
            content={
                "message": "The ingreso was successfully created",
                "data": jsonable_encoder(new_ingreso),
            },
            status_code=status.HTTP_201_CREATED,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@ingreso_router.put(
    "/{id}",
    tags=["ingresos"],
    response_model=dict,
    description="Updates the data of specific ingreso",
)
def update_ingreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
    ingreso: Ingreso = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        element = IngresoRepository(db).update_ingreso(id, ingreso)
        return JSONResponse(
            content={
                "message": "The ingreso was successfully updated",
                "data": jsonable_encoder(element),
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@ingreso_router.delete(
    "/{id}",
    tags=["ingresos"],
    response_model=dict,
    description="Removes specific ingreso",
)
def remove_ingreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        IngresoRepository(db).delete_ingreso(id)
        return JSONResponse(
            content={"message": "The ingreso was removed successfully", "data": None},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
