from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from src.config.database import Base
from sqlalchemy import Enum
from sqlalchemy.sql import func

class Egreso(Base):
    __tablename__ = "egresos"
    id          =   Column(Integer, primary_key=True, autoincrement=True)
    fecha       =   Column(DateTime(timezone=True), server_default=func.now())
    descripcion =   Column(String(length=64))
    valor       =   Column(Float, index=True)
    categoria   =   Column(Enum("alimentacion", "transporte", "ocio", "libros"))