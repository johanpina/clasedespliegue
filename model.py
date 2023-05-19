
from sqlalchemy import Column, Integer, String
from database import Base


class LibroDB(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String, index=True)
    publicacion = Column(Integer)

