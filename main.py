from fastapi import FastAPI
from src.middlewares.error_handler import ErrorHandler
from src.schemas.ingreso import Ingreso
from src.schemas.egreso import Egreso
from src.routers.ingresos import ingreso_router
from src.routers.egresos import egresos_router


app = FastAPI()

app.title = "Control gastos API"
app.summary = "Control gastos REST API with FastAPI and Python"
app.description = "This is a demostration of API REST using Python"
app.version = "0.0.1"

app.openapi_tags = [
    {
        "name": "web",
        "description": "Endpoints of example",
    },
    {
        "name": "Ingreso",
    },
    {
        "name": "Egreso",
    },
]

app.add_middleware(ErrorHandler)
app.include_router(prefix="/ingresos", router=ingreso_router)
app.include_router(prefix="/egresos", router=egresos_router)

contador = 0
egresos = []
ingresos = []

@app.get("/api/v1")
def great():
    return {"Hello": "World"}
        
