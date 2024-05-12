from fastapi import FastAPI
from src.middlewares.error_handler import ErrorHandler
from src.routers.ingresos import ingreso_router
from src.routers.egresos import egreso_router
from src.routers.reportes import reportes_router
from src.config.database import Base, engine
from src.routers.auth import auth_router

app = FastAPI()

app.title = "Control gastos API"
app.summary = "Control gastos REST API with FastAPI and Python"
app.description = "This is a demostration of API REST using Python"
app.version = "0.1.0"

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
    {
        "name": "auth",
        "description": "User's authentication",
    },
]

app.add_middleware(ErrorHandler)
app.include_router(prefix="/api/v1/ingresos", router=ingreso_router)
app.include_router(prefix="/api/v1/egresos", router=egreso_router)
app.include_router(prefix="/api/v1/reporte", router=reportes_router)
app.include_router(prefix="", router=auth_router)
Base.metadata.create_all(bind=engine)

contador = 0
egresos = []
ingresos = []


@app.get("/api/v1")
def great():
    return {"Hello": "World"}
