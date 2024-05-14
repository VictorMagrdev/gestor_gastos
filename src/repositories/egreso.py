from typing import List
from src.models.egreso import Egreso
from src.schemas.egreso import Egreso as EgresoSchema


class EgresoRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_egresos(
        self, min_valor: float, max_valor: float, offset: int, limit: int, id: int
    ) -> List[EgresoSchema]:
        query = self.db.query(Egreso).filter(Egreso.owner_id == id)
        if min_valor is not None:
            query = query.filter(Egreso.valor >= min_valor)
        if max_valor is not None:
            query = query.filter(Egreso.valor < max_valor)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def get_egreso(self, id: int) -> EgresoSchema:
        element = self.db.query(Egreso).filter(Egreso.id == id).first()
        return element

    def create_egreso(self, egreso: EgresoSchema) -> dict:
        new_egreso = Egreso(**egreso.model_dump())
        self.db.add(new_egreso)
        self.db.commit()
        self.db.refresh(new_egreso)
        return new_egreso

    def update_egreso(self, id: int, egreso: EgresoSchema) -> dict:
        element = self.db.query(Egreso).filter(Egreso.id == id).first()
        element.descripcion = egreso.descripcion
        element.valor = egreso.valor
        element.categoria = egreso.categoria
        self.db.commit()
        self.db.refresh(element)
        return element

    def delete_egreso(self, id: int) -> dict:
        element: Egreso = self.db.query(Egreso).filter(Egreso.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
