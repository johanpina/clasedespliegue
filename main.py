from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, Base, engine
from schemas import Libro, LibroBase
from model import LibroDB
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List 

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI() 

@app.post("/libros/", response_model=Libro)
async def crear_libro(libro: LibroBase, db: Session = Depends(get_db)):
    db_libro = LibroDB(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@app.delete("/libros/{id_libro}")
async def eliminar_libro(id_libro: int, db: Session = Depends(get_db)):
    try:
        libro = db.query(LibroDB).filter(LibroDB.id == id_libro).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado"}

@app.get("/libros/{id_libro}", response_model=Libro)
async def leer_libro(id_libro: int, db: Session = Depends(get_db)):
    try:
        libro = db.query(LibroDB).filter(LibroDB.id == id_libro).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.get("/libros/", response_model=List[Libro])
async def listar_libros(db: Session = Depends(get_db)):
    libros = db.query(LibroDB).all()
    return libros