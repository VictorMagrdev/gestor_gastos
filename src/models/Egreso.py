from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from src.config.database import Base


class Egreso(Base):
    __tablename__ = "egresos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(min_length=4, max_length=64), index=True)
    price = Column(Float(), index=True)
    expiration = Column(Date, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")
