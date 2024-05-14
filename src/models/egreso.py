from sqlalchemy import Column, Date, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from src.config.database import Base
from sqlalchemy import Enum


class Egreso(Base):
    __tablename__ = "egresos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date)
    descripcion = Column(String(length=64))
    valor = Column(Float, index=True)
    categoria = Column(Enum("alimentacion", "transporte", "ocio", "libros"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="egresos")
