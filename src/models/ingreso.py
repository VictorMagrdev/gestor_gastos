from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from src.config.database import Base
from sqlalchemy import Enum


class Ingreso(Base):
    __tablename__ = "ingresos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date)
    descripcion = Column(String(length=64))
    valor = Column(Float, index=True)
    categoria = Column(
        Enum("Pago de nomina", "Pago contrato", "Pago arriendo", "Mesada")
    )
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="ingresos")
