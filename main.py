from datetime import datetime, time, timedelta
from typing import Annotated
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import Any, Optional, List


app = FastAPI()


@app.get("/")
def great():
    return {"Hello": "World"}

class Ingreso(BaseModel):
    id:                 int | None = Field(default=None, primary_key=True)
    fecha:              Annotated[datetime | None, Body()] = Field(title="entry transaction date")
    descripcion:        str = Field(min_length=4, max_length=64, title="entry transaction description")
    valor:              float = Field(default="1000", le=5000000, lg=100, title="Price of entry transaction")
    categoria:          str = Field(min_length=4, max_length=128, title="category of entry transaction")