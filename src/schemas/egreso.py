from pydantic import BaseModel, Field, validator

egreso_categorias = ["alimentacion", "transporte", "ocio", "libros"]


class Egreso(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    fecha: str | None = Field(default=None, title="Entry transaction date")
    descripcion: str = Field(
        min_length=4, max_length=64, title="entry transaction description"
    )
    valor: float = Field(
        default="1000", le=5000000, lg=100, title="Price of entry transaction"
    )
    categoria: str = Field(
        min_length=4, max_length=128, title="category of entry transaction"
    )

    @validator("categoria")
    @classmethod
    def validar_categoria_egreso(cls, categoria):
        if categoria not in egreso_categorias:
            raise ValueError("Categoria incorrecta para los egresos")
        return categoria
