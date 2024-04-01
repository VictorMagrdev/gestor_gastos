from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import Any, Optional, List


app = FastAPI()


@app.get("/")
def great():
    return {"Hello": "World"}