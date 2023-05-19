from pydantic import BaseModel

class LibroBase(BaseModel):
    titulo: str
    autor: str
    publicacion: int

class Libro(LibroBase):
    id: int

    class Config:
        orm_mode = True

