from pydantic import BaseModel, Field, validator
from datetime import date

ingresos_categorias = ["Pago de nomina", "Pago contrato", "Pago arriendo", "Mesada"]


class Ingreso(BaseModel):
    id: int = Field(default=None, primary_key=True)
    fecha: str = Field(default=None, title="Entry transaction date")
    descripcion: str = Field(
        min_length=4, max_length=64, title="entry transaction description"
    )
    valor: float = Field(
        default="1000", le=5000000, lg=100, title="Price of entry transaction"
    )
    categoria: str = Field(
        min_length=4, max_length=128, title="category of entry transaction"
    )
    owner_id: int = Field(ge=1, title="Owner of the ingreso")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "fecha": "2025-04-04",
                "descripcion": "uvuvwewewe",
                "valor": 5000,
                "categoria": "Mesada",
                "owner_id": 1,
            }
        }

    @validator("categoria")
    @classmethod
    def validar_categoria_ingreso(cls, categoria):
        if categoria not in ingresos_categorias:
            raise ValueError("Categoria incorrecta para los ingresos")
        return categoria


class IngresoCreate(BaseModel):
    fecha: date = Field(default=None, title="Entry transaction date")
    descripcion: str = Field(
        min_length=4, max_length=64, title="entry transaction description"
    )
    valor: float = Field(
        default="1000", le=5000000, lg=100, title="Price of entry transaction"
    )
    categoria: str = Field(
        min_length=4, max_length=128, title="category of entry transaction"
    )
