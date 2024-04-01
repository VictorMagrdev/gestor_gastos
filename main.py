from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import Any, Optional, List

from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

app = FastAPI()


@app.get("/")
def great():
    return {"Hello": "World"}

class Egreso(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    fecha: Annotated[datetime | None, Body()] = None
    descripcion: str = Field(min_length=4, max_length=64, title="email of the user")
    valor: float = Field(default="0", le=5000000, lg=100, title="Price of the product")
    categoria: str = Field(min_length=4, max_length=128, title="password of the user")