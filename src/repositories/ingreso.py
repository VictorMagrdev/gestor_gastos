from typing import List
from src.models.ingreso import Ingreso
from src.schemas.ingreso import Ingreso as IngresoSchema, IngresoCreate

class IngresoRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_ingresos(
        self, min_valor: float, max_valor: float, offset: int, limit: int, id: int
    ) -> List[IngresoSchema]:
        query = self.db.query(Ingreso).filter(Ingreso.owner_id == id)
        if min_valor is not None:
            query = query.filter(Ingreso.valor >= min_valor)
        if max_valor is not None:
            query = query.filter(Ingreso.valor < max_valor)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def get_ingreso(self, id: int) -> IngresoSchema:
        element = self.db.query(Ingreso).filter(Ingreso.id == id).first()
        return element

    def create_ingreso(self, ingreso: IngresoCreate, id: int) -> dict:
        new_ingreso = Ingreso(**ingreso.model_dump())
        new_ingreso.owner_id = id
        self.db.add(new_ingreso)
        self.db.commit()
        self.db.refresh(new_ingreso)
        return new_ingreso

    def update_ingreso(self, id: int, ingreso: IngresoSchema) -> dict:
        element = self.db.query(Ingreso).filter(Ingreso.id == id).first()
        element.descripcion = ingreso.descripcion
        element.valor = ingreso.valor
        element.categoria = ingreso.categoria
        self.db.commit()
        self.db.refresh(element)
        return element

    def delete_ingreso(self, id: int) -> dict:
        element: Ingreso = self.db.query(Ingreso).filter(Ingreso.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
